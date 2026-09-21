"""NETCONF Schemas."""

from ncclient.operations.rpc import RPCError
from nornir.core.task import List, Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import SchemaResult, write_output


def _schema_content(schema_reply: object) -> str:
    """Return the raw YANG content parsed by ncclient."""
    data = getattr(schema_reply, "data", None)
    if isinstance(data, str):
        return data
    return str(schema_reply)


def netconf_get_schemas(task: Task, schemas: List[str], schema_path: str) -> Result:  # nosec
    """Fetch provided schemas and write to a file inside of a given directory path, `schema_path`.

    All schemas will be written to a file in the `schema_path` directory provided and
    named by the schema name.

    Any errors on extracting the schema will be logged in the result object.

    Args:
        schemas (List[str]): List of schemas to fetch.
        schema_path (str): Directory path to save schemas output.

    Simple Example ::

        > nr.run(task=netconf_schemas, schemas=["schema1", "schema2"], schema_path="workdir/schemas")

    Returns:
        Result object with the following attributes set::

          * result (SchemaResult): List of files created, errors, if any and base directory path.
    """
    manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    result = SchemaResult(directory=schema_path)

    for schema in schemas:
        try:
            schema_reply = manager.get_schema(schema)
            write_output(_schema_content(schema_reply), path=schema_path, filename=schema, ext="yang")
            result.files.append(f"{schema_path}/{schema}.yang")
        except RPCError as err_ex:
            result.errors.append(str(err_ex).strip())

    return Result(host=task.host, result=result)
