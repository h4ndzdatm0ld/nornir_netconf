"""NETCONF capabilities."""
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import RpcResult


def netconf_capabilities(task: Task) -> Result:
    """Gather Netconf capabilities from device.

    Examples:
        Simple example::

            > nr.run(task=netconf_capabilities)

    Returns:
        Result object with the following attributes set::

            * result (RpcResult): Rpc and Manager
    """
    manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    capabilities = manager.server_capabilities
    rpc_result = RpcResult(rpc=capabilities, manager=manager)
    return Result(host=task.host, result=rpc_result)
