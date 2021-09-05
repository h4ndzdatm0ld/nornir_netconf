"""NETCONF capabilities."""
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME


def netconf_capabilities(task: Task) -> Result:
    """Gather Netconf capabilities from device.

    Examples:
        Simple example::

            > nr.run(task=netconf_capabilities)

    Returns:
        Result object with the following attributes set:
          * result (``list``): list with the capabilities of the host
    """
    failed = False
    manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    capabilities = list(manager.server_capabilities)
    return Result(host=task.host, failed=failed, result=capabilities)
