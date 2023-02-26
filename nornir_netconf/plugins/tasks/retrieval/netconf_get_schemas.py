"""NETCONF Schemas."""
from ncclient.operations.rpc import RPCError
from nornir.core.task import List, Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import SchemaResult, write_output


def netconf_get_schemas(task: Task, schemas: List[str], schema_path: str) -> Result:  # nosec
    """Fetch provided schemas and write to a file inside of a given directory path, `schema_path`.

    All schemas will be written to a file in the `schema_path` directory provided and
    named by the schema name.

    Any errors on extracting the schema will be logged in the result object.

    Args:
        schemas (List[str]): List of schemas to fetch.
        schema_path (str): Directory path to save schemas output.

    Examples::

        > nr.run(task=netconf_schemas, schemas=["schema1", "schema2"])
        > nr.run(task=netconf_schemas, schemas=["schema1", "schema2"], schema_path="workdir/schemas")

    Returns:
        Result: Result
    """
    manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    result = SchemaResult(directory=schema_path)

    for schema in schemas:
        try:
            write_output(manager.get_schema(schema).data_xml, path=schema_path, filename=schema)
            result.files.append(f"{schema_path}/{schema}.txt")
        except RPCError as err_ex:
            result.errors.append(str(err_ex).strip())

    return Result(host=task.host, result=result)
