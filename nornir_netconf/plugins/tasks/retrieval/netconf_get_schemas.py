"""NETCONF Schemas."""

from pathlib import Path

from ncclient.operations.rpc import RPCError
from nornir.core.task import List, Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import SchemaResult, write_output


def _schema_content(schema_reply: object) -> str:
    """Return the raw YANG content parsed by ncclient."""
    data = getattr(schema_reply, "data", None)
    if not isinstance(data, str) or not data.strip():
        raise ValueError("NETCONF get-schema reply did not contain schema text.")
    return data


def _schema_filename(schema: str) -> str:
    """Reject schema identifiers that could escape the output directory."""
    if not schema or schema in {".", ".."} or Path(schema).name != schema or "\\" in schema:
        raise ValueError(f"Invalid schema identifier: {schema!r}")
    return schema


def netconf_get_schemas(task: Task, schemas: List[str], schema_path: str) -> Result:  # nosec
    """Fetch provided schemas and write to a file inside of a given directory path, `schema_path`.

    Each schema's raw YANG text will be written to the `schema_path` directory and
    named by the schema identifier.

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
            filename = _schema_filename(schema)
            schema_reply = manager.get_schema(schema)
            write_output(_schema_content(schema_reply), path=schema_path, filename=filename, ext="yang")
            result.files.append(f"{schema_path}/{filename}.yang")
        except (RPCError, ValueError) as err_ex:
            result.errors.append(str(err_ex).strip())

    return Result(host=task.host, result=result)
