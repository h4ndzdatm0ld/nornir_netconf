"""NETCONF edit config."""
from typing import Optional

from ncclient.manager import Manager
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import RpcResult
from nornir_netconf.plugins.helpers.rpc_helpers import check_capability


def netconf_edit_config(
    task: Task,
    config: str,
    target: str = "running",
    manager: Optional[Manager] = None,
    default_operation: Optional[str] = None,
) -> Result:
    """Edit configuration of device using Netconf.

    Arguments:
        config: Configuration snippet to apply
        target: Target configuration store
        manager: class:: ncclient.manager.Manager
        default_operation (str): merge, replace or None

    Examples:
        Simple example::

            > nr.run(task=netconf_edit_config, config=desired_config)

    Returns:
        Result
    """
    error = None
    result = None
    manager = None

    if default_operation not in ["merge", "replace", None]:
        raise ValueError(f"{default_operation} not supported.")
    if not manager:
        manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    if target in ["candidate", "startup"]:
        capabilities = list(manager.server_capabilities)
        if not check_capability(capabilities, target):
            raise ValueError(f"{target} datastore is not supported.")
    try:
        result = manager.edit_config(config, target=target, default_operation=default_operation)
    except Exception as rpc_error:
        error = rpc_error

    result = RpcResult(rpc=result, manager=manager, error=error)
    return Result(host=task.host, result=result)
