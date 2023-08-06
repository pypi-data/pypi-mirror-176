from jobsworthy.util import error

messages = {
    'table_name_not_configured': """Table_name class property not provided""",

    'error_identity_merge_condition_not_implemented': """The repository requires an identity_merge_condition function 
    to perform a delta merge. This function takes the name of the baseline and the name of the updates used in the merge.
    Return a delta table condition that contains an identity column name (or sub column name). """,

    'df_not_in_stream': """Dataframe is not in a Stream.  Can't write stream.""",

    'writing_stream_without_setting_writer': """Attempting to write to a stream without setting up a stream writer.
    When constructing the hive repo set the stream_writer attribute using either add hive_repo.StreamHiveWriter
    or hive_repo.StreamFileWriter.""",

    'temp_table_not_configured': """temp_table_name class property not provided""",

    'hive_stream_writer_not_available': """hive_repo.StreamHiveWriter can not be used (probably because in Test), use 
    hive_repo.StreamFileWriter instead.""",

    'no_schema_provided_on_create_df': """Called create_df without either providing a schema or implementing the 
    schema() function.""",

    'checkpoint_root_not_supported': """Jobsworthy: use of checkpoint_root not supported since version 0.4.0.  
    Use db_path_override_for_checkpoint instead.""",

    'checkpoint_override_must_be_supported_in_test': """Configuration of db_path_override_for_checkpoint must be 
    provided when in testing and when using delta table operations.  To disable this exception remove the call to 
    running_in_test() from the JobConfig."""
}


def checkpoint_root_not_supported():
    raise error.RepoConfigError(messages[checkpoint_root_not_supported.__name__])


def table_name_not_configured():
    return error.RepoConfigError(messages[table_name_not_configured.__name__])


def error_identity_merge_condition_not_implemented():
    return error.RepoConfigError(messages[error_identity_merge_condition_not_implemented.__name__])


def df_not_in_stream():
    return error.NotAStreamError(messages[df_not_in_stream.__name__])


def writing_stream_without_setting_writer():
    return error.RepoConfigError(writing_stream_without_setting_writer.__name__)


def temp_table_not_configured():
    return error.RepoConfigError(temp_table_not_configured.__name__)


def hive_stream_writer_not_available():
    return error.RepoConfigError(hive_stream_writer_not_available.__name__)


def no_schema_provided_on_create_df():
    return error.RepoWriteError(no_schema_provided_on_create_df.__name__)


def checkpoint_override_must_be_supported_in_test():
    return error.RepoConfigError(checkpoint_override_must_be_supported_in_test.__name__)