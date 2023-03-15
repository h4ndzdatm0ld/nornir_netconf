"""NETCONF validate config."""
from typing import Optional

from ncclient.manager import Manager
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import RpcResult


def netconf_validate(
    task: Task,
    source: Optional[str] = "candidate",
    manager: Optional[Manager] = None,
) -> Result:
    """Validate the datastore configuration.

    Arguments:
        source (str): Source configuration store
        manager (Manager): NETCONF Manager

    Examples:
        Simple example::

            > nr.run(task=netconf_validate)

    Returns:
        Result object with the following attributes set::

            * result (RpcResult): Rpc and Manager
    """
    if not manager:
        manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    result = manager.validate(source=source)
    rpc_result = RpcResult(rpc=result, manager=manager)
    return Result(host=task.host, result=rpc_result)
