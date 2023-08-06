from typing import Protocol
from jobsworthy import spark_job
from jobsworthy.util import error, logger


class DbNamingConventionProtocol(Protocol):

    def database_name(self) -> str:
        """
        The database name is provide in the dbconfig section of the job config.  This function returns that name.
        :return:
        """
        ...

    def db_table_name(self, table_name) -> str:
        """
        This function combines the database name and the provided table name.

        Used when using hive-based operations; like drop table, or spark.table(db_table_name("t1")

        Used by:
        + HiveTableReader().read
        + HiveRepo().drop_table_by_name
        + HiveRepo().read_stream
        + HiveRepo().create
        + HiveRepo().get_table_properties
        + HiveRepo().add_to_table_properties
        + HiveRepo().remove_from_table_properties

        :param table_name:
        :return:
        """
        ...

    def db_path(self) -> str:
        """
        Provide the location path for a database.  Used when creating or dropping the database.
        :return:
        """
        ...

    def db_table_path(self, table_name: str) -> str:
        """
        The path location of the table.
        :param table_name:
        :return:
        """
        ...

    def delta_table_location(self, table_name: str) -> str:
        """
        The load location for reading a delta table using DeltaTable class.

        DeltaTable.forPath(spark, self.delta_table_location)

        Used by Hive functions:
        + DeltaTableReader().table
        + DeltaFileReader().read
        + StreamFileWriter().write


        :param table_name:
        :return:
        """
        ...

    def checkpoint_location(self, table_name) -> str:
        """
        The location of the checkpoint folder when using delta streaming.

        :param table_name:
        :return:
        """
        ...


class DbNamingConventionCallerDefined(DbNamingConventionProtocol):
    """
    DB and Table naming convention on the path configurations provided in dbconfig.  Uses the following properties
    from the config:

        cfg = (spark_job.JobConfig()
              .configure_hive_db(db_name="my_db",
                                 db_file_system_path_root="domains/my_domain/data_products/my_data_product_name",
                                 db_path_override_for_checkpoint="spark-warehouse/domains/my_domain/data_products/my_data_product_name"))

    That is, the paths are explicitly defined in the dbconfig, rather than constructed using the job configuration.
    """

    checkpoint_folder = "_checkpoint"

    def __init__(self, job_config: spark_job.JobConfig):
        self.config = job_config

    def database_name(self):
        return self.config.db.db_name

    def db_table_name(self, table_name):
        return f"{self.database_name()}.{table_name}"

    def db_file_system_path_root(self):
        return self.config.db.db_file_system_root

    def db_path(self):
        """
        Used to define the location of a Hive table.  The DB Path is formatted as follows:

        <dbconfig.db_file_system_path_root>/<database_name>.db
        """
        if not self.db_file_system_path_root():
            raise error.RepoConfigError(
                message="Jobsworth: db path not configured.  Set db_file_system_path_root on the HIVE config")

        if self.db_file_system_path_root()[-1] == "/":
            logger.info(msg="Jobsworth: WARNING. db_file_system_path_root should not end with a '/'")
            return f"{self.db_file_system_path_root()[:-1]}/{self.database_name()}.db"

        return f"{self.db_file_system_path_root()}/{self.database_name()}.db"

    def db_table_path(self, table_name: str) -> str:
        """
        The db_path with the table name appended.  Used when defining the location for a table in the Hive store.
        :param table_name:
        :return:
        """
        return f"{self.db_path()}/{table_name}"


    def delta_table_location(self, table_name):
        """
        The delta table location (when using the spark context to load a delta table).  Takes into account  delta tables
        with a checkpoint location (when using Delta stream to write data).  On the cluster there is no need to override
        the checkpoint location (it is db_file_system_path_root from the config).  However, when running the tests the
        location needs to be overridden by appending "spark-warehouse" to the relative name of the
        db_file_system_path_root.

        On the cluster, the config looks something like this:

        JobConfig().configure_hive_db(db_name="my_db",
                                      db_file_system_path_root="/domain/my_domain/my_data_product_name")

        Note the absolute path.  If using a relative path, the table is associated with the default databaricks
        table path.  For example /dbfs/user/hive/warehouse

        For testing the override needs to be used.

        JobConfig().configure_hive_db(db_name="my_db",
                                      db_file_system_path_root="domains/my_domain/my_data_product_name",
                                      db_path_override_for_checkpoint="spark-warehouse/domain/my_domain/my_data_product_name")

        Note the use of relative paths and prepending of "spark-warehouse"

        """
        return f"{self.db_file_root_or_checkpoint_override()}/{self.database_name()}.db/{table_name}"

    def db_file_root_or_checkpoint_override(self):
        if self.config.db.db_path_override_for_checkpoint:
            return self.config.db.db_path_override_for_checkpoint
        return self.db_file_system_path_root()


    def checkpoint_location(self, table_name):
        """
        The checkpoint location is defined using the delta_table_location (see above) with the constant "_checkpoint"
        appended.
        """
        return f"{self.delta_table_location(table_name)}/{self.checkpoint_folder}"


class Db:

    def __init__(self, session,
                 job_config: spark_job.JobConfig,
                 naming_convention: DbNamingConventionProtocol = DbNamingConventionCallerDefined):
        self.session = session
        self.config = job_config
        self.naming_convention = naming_convention(self.config)
        self.create_db_if_not_exists()

    def create_db_if_not_exists(self):
        self.session.sql(
            f"create database IF NOT EXISTS {self.naming().database_name()} LOCATION '{self.naming().db_path()}'")

    def drop_db(self):
        self.session.sql(f"drop database IF EXISTS {self.naming().database_name()} CASCADE")
        return self

    def db_exists(self) -> bool:
        return self.session.catalog.databaseExists(self.naming().database_name())

    def table_exists(self, table_name):
        return table_name in self.list_tables()

    def catalog_table_exists(self, table_name):
        return self.session.catalog.tableExists(table_name)

    def list_tables(self):
        return [table.name for table in self.session.catalog.listTables(self.naming().database_name())]

    def table_format(self):
        return self.config.db.table_format

    def naming(self):
        return self.naming_convention
