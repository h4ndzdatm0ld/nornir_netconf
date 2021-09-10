"""NETCONF edit config."""
from typing import Optional

from ncclient.manager import Manager
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers.rpc_helpers import get_result, check_capability


def netconf_edit_config(
    task: Task,
    config: str,
    target: str = "running",
    manager: Optional[Manager] = None,
    xmldict: bool = False,
    default_operation: Optional[str] = None,
) -> Result:
    """Edit configuration of device using Netconf.

    Arguments:
        config: Configuration snippet to apply
        target: Target configuration store
        manager: class:: ncclient.manager.Manager
        xmldict (boolean): convert xml to dict
        default_operation (str): merge, replace or None

    Examples:
        Simple example::

            > nr.run(task=netconf_edit_config, config=desired_config)

    Returns:
        Result
    """
    if default_operation not in ["merge", "replace", None]:
        raise ValueError(f"{default_operation} not supported.")
    if not manager:
        manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    if target in ["candidate", "startup"]:
        capabilities = list(manager.server_capabilities)
        print(capabilities)
        if not check_capability(capabilities, target):
            raise ValueError(f"{target} datastore is not supported.")
    result = manager.edit_config(config, target=target, default_operation=default_operation)
    return Result(host=task.host, **get_result(result, xmldict))
