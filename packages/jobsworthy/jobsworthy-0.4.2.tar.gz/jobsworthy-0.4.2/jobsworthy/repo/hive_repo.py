import uuid
from typing import Optional, Dict

import pyspark.sql.streaming
from pyspark.sql import dataframe
from pyspark.sql import functions as F
from delta.tables import *
from functools import reduce

from . import spark_db, repo_messages
from jobsworthy.util import error, monad


class TableProperty:
    @classmethod
    def table_property_expression(cls, set_of_props: List):
        return ",".join([prop.format_as_expression() for prop in set_of_props])

    @classmethod
    def table_property_expression_keys(cls, set_of_props: List):
        return ",".join([prop.format_key_as_expression for prop in set_of_props])

    def __init__(self, key: str, value: str):
        self.key = self.prepend_urn(key)
        self.value = value

    def prepend_urn(self, key):
        if key[0:3] == 'urn':
            return key
        return f"urn:{key}"

    def __key(self):
        return (self.key, self.value)

    def __hash__(self):
        return hash((self.key, self.value))

    def __eq__(self, other):
        return self.__key() == other.__key()

    def format_as_expression(self):
        return f"'{self.key}'='{self.value}'"

    def format_key_as_expression(self):
        return f"'{self.key}'"


class StreamFileWriter:

    def write(self, repo, stream, table_name=None):
        table_name = table_name if table_name else repo.table_name
        return stream.start(repo.delta_table_location(table_name))


class StreamHiveWriter:
    """
    This is the stream writer to be used on the cluster.  This capability is not supported in local test mode.
    Use StreamFileWriter instead
    """

    def write(self, repo, stream, table_name=None):
        if not hasattr(stream, 'table'):
            raise repo_messages.hive_stream_writer_not_available()

        table_name = table_name if table_name else repo.table_name
        return stream.table(repo.db_table_name(table_name))


class DeltaFileReader:
    """
    Reader which reads a delta table from a known table location (table path) using the Spark session.
    """

    def read(self, repo, table_name=None):
        return (repo.db.session.read
                .format('delta')
                .load(repo.delta_table_location(table_name if table_name else repo.table_name)))


class DeltaTableReader:
    """
    Delta reader using the DeltaTable class
    """

    def read(self, repo, table_name=None) -> Optional[dataframe.DataFrame]:
        if not repo.table_exists():
            return None
        return self.table(repo, table_name).toDF()

    #
    def table(self, repo, table_name=None) -> DeltaTable:
        return DeltaTable.forPath(repo.db.session,
                                  repo.delta_table_location(table_name if table_name else repo.table_name))


class HiveTableReader:
    """
    The default table Reader.  Reads data from a Hive database and table location.
    """

    def read(self, repo, table_name=None):
        table_name = table_name if table_name else repo.table_name

        if not repo.table_exists(table_name):
            return None
        return repo.db.session.table(repo.db_table_name(table_name))


class HiveRepo:
    default_stream_trigger_condition = {'once': True}

    def __init__(self,
                 db: spark_db.Db,
                 stream_writer=None,
                 reader=HiveTableReader):
        self.db = db
        self.stream_writer = stream_writer
        self.reader = reader
        self.stream_query = None
        if not hasattr(self, "table_name") or not self.__class__.table_name:
            raise repo_messages.table_name_not_configured()

    #
    # Table Lifecycle Events
    #
    def table_exists(self, table_name=None) -> bool:
        table_name = table_name if table_name else self.table_name
        return self.db.table_exists(table_name)

    def drop_table(self):
        """
        Drops the table if it exists.  Use carefully!
        :return:
        """
        return self.drop_table_by_name()

    def drop_table_by_name(self, table_to_drop: str = None):
        """
        By default drops the main table representing the repo (that is self.table_name).
        However, when dropping the temporary table (or other associated tables), provide the
        table name.
        :return:
        """
        dropped_table = table_to_drop if table_to_drop else self.table_name
        self.db.session.sql(f"DROP TABLE IF EXISTS {self.db_table_name(dropped_table)}")
        return self

    def drop_temp_table(self):
        if not hasattr(self, "temp_table_name") or not self.__class__.temp_table_name:
            raise repo_messages.temp_table_not_configured()

        return self.drop_table_by_name(table_to_drop=self.temp_table_name)

    #
    # Table Read Functions
    #

    def delta_read(self) -> Optional[dataframe.DataFrame]:
        if not self.table_exists():
            return None
        return DeltaTableReader().read(self, self.table_name)

    def delta_table(self, table_name=None) -> DeltaTable:
        return DeltaTableReader().table(self, table_name if table_name else self.table_name)

    def read(self, target_table_name: str = None) -> Optional[dataframe.DataFrame]:
        return self.reader().read(self, target_table_name)

    def read_stream(self) -> DataFrame:
        return (self.db.session
                .readStream
                .format('delta')
                .option('ignoreChanges', True)
                .table(self.db_table_name()))

    #
    # Table Write Functions
    #
    def create_df(self, data, schema=None):
        return self.db.session.createDataFrame(data=data,
                                               schema=self.determine_schema_to_use(schema))

    def determine_schema_to_use(self, schema_from_argument=None):
        if schema_from_argument:
            return schema_from_argument
        if hasattr(self, "schema") and self.schema():
            return self.schema()
        raise repo_messages.no_schema_provided_on_create_df()

    @monad.monadic_try(error_cls=error.RepoWriteError)
    def try_write_stream(self, stream, partition_cols: tuple = tuple(), trigger: dict = None):
        return self.write_stream(stream, partition_cols, trigger)

    def write_stream(self, stream, partition_cols: tuple = tuple(), trigger: dict = None):
        """
        Write a stream.  Provide a stream.
        + To create partition columns in the table, provide a tuple of column names, the default is no partitioning
        + The default trigger action is {'once': True}. see
          https://spark.apache.org/docs/3.1.1/api/python/reference/api/pyspark.sql.streaming.DataStreamWriter.trigger.html
          for more details.
        """
        trigger_condition = trigger if trigger else self.__class__.default_stream_trigger_condition

        self.stream_query = self.write_stream_to_table(stream, self.table_name, trigger_condition, partition_cols)
        return self

    def write_stream_temporary(self, stream, partition_cols: tuple = tuple()) -> DataFrame:
        if not hasattr(self, "temp_table_name") or not self.__class__.temp_table_name:
            raise repo_messages.temp_table_not_configured()

        """
        Write a stream to dataframe.  Provide a stream.
        + Always uses the default trigger action {'once': True}. see
          https://spark.apache.org/docs/3.1.1/api/python/reference/api/pyspark.sql.streaming.DataStreamWriter.trigger.html
          for more details.
        """
        trigger_condition = self.__class__.default_stream_trigger_condition

        self.drop_temp_table()

        self.stream_query = self.write_stream_to_table(stream, self.temp_table_name, trigger_condition, partition_cols)
        self.await_termination()
        df = self.read(self.temp_table_name)
        return df

    def delta_stream_upserter(self, stream, partition_cols: tuple = tuple()):
        return DeltaStreamUpserter(self, partition_cols).execute(stream)

    def write_stream_to_table(self,
                              stream,
                              table_name: str,
                              trigger_condition,
                              partition_cols: tuple = tuple()):
        if not stream.isStreaming:
            raise repo_messages.df_not_in_stream()
        if not self.stream_writer:
            raise repo_messages.writing_stream_without_setting_writer()

        return self.stream_writer().write(self, stream
                                          .writeStream
                                          .format('delta')
                                          .partitionBy(partition_cols)
                                          .option('checkpointLocation',
                                                  self.db.naming().checkpoint_location(table_name))
                                          .trigger(**trigger_condition), table_name)

    @monad.monadic_try(error_cls=error.RepoWriteError)
    def try_append(self, df, partition_cols: tuple = tuple()):
        return self.append(df, partition_cols)

    def append(self, df, partition_cols: tuple = tuple()):
        """
        Executes a simple append operation on a table using the provided dataframe.
        + Optionally provide a tuple of columns for partitioning the table.
        """

        return self.create(df, partition_cols)

    def create(self, df, partition_cols: tuple = tuple()):
        """
        Executes a simple append operation on a table using the provided dataframe.
        + Optionally provide a tuple of columns for partitioning the table.
        """
        result = (df.write
                  .format(self.db.table_format())
                  .partitionBy(partition_cols)
                  .mode("append")
                  .saveAsTable(self.db_table_name()))
        self.merge_table_properties()
        return result

    @monad.monadic_try(error_cls=error.RepoWriteError)
    def try_upsert(self, df, partition_puning_col: str = None, partition_cols: tuple = tuple()):
        """
        The try_upsert wraps the upsert function with a Try monad.  The result will be an Either.  A successful result
        usually returns Right(None).
        """
        return self.upsert(df, partition_puning_col, partition_cols)

    def upsert(self, df, partition_pruning_col: str = None, partition_cols: tuple = tuple()):
        """
        Upsert performs either a create or a delta merge.  The create is called when the table doesnt exist.  Otherwise
        a delta merge is performed.
        + partition_pruning_col.  When partitioning, the merge will use one of the partition columns to execute a merge using
          partition pruning.
        + Optionally provide partition columns as a tuple of column names.

        Note that the merge requires that the repository implement a identity_merge_condition function when using merge
        operations.  This is a merge condition that identifies the upsert identity.
        """
        if not self.table_exists():
            return self.create(df, partition_cols)

        (self.delta_table().alias(self.table_name)
         .merge(
            df.alias('updates'),
            self.build_merge_condition(self.table_name, 'updates', partition_pruning_col)
        )
         .whenNotMatchedInsertAll()
         .whenMatchedUpdateAll()
         .execute())

    #
    # Streaming Functions
    #
    def await_termination(self, other_stream_query=None):
        target_stream = other_stream_query if other_stream_query else self.stream_query
        if not target_stream:
            return None

        target_stream.awaitTermination()
        return self

    #
    # Utility Functions
    #
    def build_merge_condition(self, name_of_baseline, update_name, partition_pruning_col):
        if not hasattr(self, 'identity_merge_condition'):
            raise repo_messages.error_identity_merge_condition_not_implemented()

        pruning_cond = self.build_puning_condition(name_of_baseline, update_name, partition_pruning_col)

        identity_cond = self.identity_merge_condition(name_of_baseline, update_name)

        return f"{pruning_cond}{identity_cond}"

    def build_puning_condition(self, name_of_baseline, update_name, partition_puning_col):
        if partition_puning_col:
            return f"{name_of_baseline}.{partition_puning_col} = {update_name}.{partition_puning_col} AND "
        return ""

    def build_upsert_match_fn(self, update_name: str, match_col: str) -> str:
        return f"{update_name}.{match_col} = {self.table_name}.{match_col}"

    #
    # Table Naming Functions
    #
    def db_table_name(self, table_name=None):
        return self.db.naming().db_table_name(table_name if table_name else self.table_name)

    def db_temp_table_name(self):
        return self.db.naming().db_table_name(self.temp_table_name)

    def db_table_path(self, table_name=None):
        return self.db.naming().db_table_path(table_name if table_name else self.table_name)

    def delta_table_location(self, table_name=None):
        if (self.db.config.is_running_in_test and
                not self.db.config.db.db_path_override_for_checkpoint):
            raise repo_messages.checkpoint_override_must_be_supported_in_test()
        return self.db.naming().delta_table_location(table_name if table_name else self.table_name)

    #
    # Table Property Functions
    #
    def merge_table_properties(self):
        if not hasattr(self, 'table_properties'):
            return self
        set_on_table = set(self.urn_table_properties())

        self.add_to_table_properties(set(self.__class__.table_properties) - set_on_table)
        self.remove_from_table_properties(set_on_table - set(self.__class__.table_properties))
        return self

    def urn_table_properties(self) -> List[TableProperty]:
        return [TableProperty(prop.key, prop.value) for prop in (self.get_table_properties()
                                                                 .filter(F.col('key').startswith('urn'))
                                                                 .select(F.col('key'), F.col('value'))
                                                                 .collect())]

    def get_table_properties(self):
        return self.db.session.sql(f"SHOW TBLPROPERTIES {self.db_table_name()}")

    def add_to_table_properties(self, to_add: List[TableProperty]):
        if not to_add:
            return self
        self.db.session.sql(
            f"alter table {self.db_table_name()} set tblproperties({TableProperty.table_property_expression(to_add)})")
        return self

    def remove_from_table_properties(self, to_remove: List[TableProperty]):
        if not to_remove:
            return self
        self.db.session.sql(
            f"alter table {self.db_table_name()} unset tblproperties({TableProperty.table_property_expression_keys(to_remove)})")
        return self

    # def __del__(self):
    #     if hasattr(self, "temp_table_name") or self.__class__.temp_table_name:
    #         self.clear_temp_storage()


class DeltaStreamUpserter:
    class TemporaryStreamDumpRepo(HiveRepo):
        table_name = "__temp__"

    def __init__(self, repo: HiveRepo, partition_cols: tuple = tuple()):
        self.repo = repo
        self.partition_cols = partition_cols
        self.temp_id = str(uuid.uuid4()).replace("-", "")
        self.temp_repo = self.TemporaryStreamDumpRepo(db=self.repo.db,
                                                      reader=DeltaFileReader,
                                                      stream_writer=StreamFileWriter)

    def execute(self, stream) -> monad.EitherMonad[DataFrame]:
        result = (monad.Right(stream)
                  >> self.drop_temp_table
                  >> self.stream_to_temp
                  >> self.await_termination
                  >> self.read_temp
                  >> self.upsert
                  >> self.drop_temp_table)
        return result

    def drop_temp_table(self, stream) -> monad.EitherMonad:
        self.repo.drop_table_by_name(self.temp_table_name(self.temp_repo.table_name))
        return monad.Right(stream)

    def stream_to_temp(self, stream) -> monad.EitherMonad:
        self.stream_query = self.temp_repo.write_stream_to_table(stream,
                                                                 self.temp_table_name(self.temp_repo.table_name),
                                                                 self.repo.__class__.default_stream_trigger_condition,
                                                                 self.partition_cols)
        return monad.Right(self.stream_query)

    def await_termination(self, stream_query) -> monad.EitherMonad[pyspark.sql.streaming.StreamingQuery]:
        self.temp_repo.await_termination(stream_query)
        return monad.Right(stream_query)

    def read_temp(self, _stream_query) -> monad.EitherMonad[DataFrame]:
        return monad.Right(self.temp_repo.read(self.temp_table_name(self.temp_repo.table_name)))

    def upsert(self, df: DataFrame) -> monad.EitherMonad[DataFrame]:
        self.repo.upsert(df, self.partition_cols[0], self.partition_cols)
        return monad.Right(df)

    def temp_table_name(self, temp_prefix):
        return f"{temp_prefix}{self.repo.table_name}__{self.temp_id}"
