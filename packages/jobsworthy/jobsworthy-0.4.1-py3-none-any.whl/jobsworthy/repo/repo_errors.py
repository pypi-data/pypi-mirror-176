from jobsworthy.util import error

class TableErrors:

    def table_name_not_configured(self):
        return error.RepoConfigError('table_name class property not provided')

    def error_identity_merge_condition_not_implemented(self):
        return error.RepoConfigError("""The repository requires an identity_merge_condition function to perform a delta
         merge. This function takes the name of the baseline and the name of the updates used in the merge.
        Return a delta table condition that contains an identity column name (or sub column name). """)

    def df_not_in_stream(self):
        return error.NotAStreamError("Dataframe is not in a Stream.  Cant write stream")

    def writing_stream_without_setting_writer(self):
        return error.RepoConfigError("""Attempting to write to a stream without setting up a stream writer.
        When constructing the hive repo set the stream_writer attribute using either add hive_repo.StreamHiveWriter
        or hive_repo.StreamFileWriter.""")


    def temp_table_not_configured(self):
        return error.RepoConfigError('temp_table_name class property not provided')

    def hive_stream_writer_not_available(self):
        return error.RepoConfigError("""hive_repo.StreamHiveWriter can not be used (probably because in Test), use 
        hive_repo.StreamFileWriter instead.""")

    def no_schema_provided_on_create_df(self):
        return error.RepoWriteError("""Called create_df without either providing a schema or implementing the 
        schema() function.""")
