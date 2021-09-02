"""NETCONF Schemas."""
from ncclient.operations.rpc import RPCError
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import write_output


def netconf_get_schemas(task: Task, schemas: list, schema_path: str = None) -> Result:
    """Fetch provided schemas and write to a file.

    Examples:
        Simple example::

            > nr.run(task=netconf_schemas)

    Returns:
        Result object with the following attributes set:
            #TODO:
    """
    manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    failed = False
    result = {"errors": [], "log": []}

    if schema_path:
        for schema in schemas:
            try:
                write_output(manager.get_schema(schema).data_xml, path=schema_path, filename=schema)
                result["log"].append(f"{schema_path}/{schema}.txt created.")
            except RPCError as err_ex:
                result["errors"].append(str(err_ex).strip())
    else:
        failed = True
        raise ValueError("Missing directory path to save Schema files.")

    return Result(host=task.host, failed=failed, result=result)
