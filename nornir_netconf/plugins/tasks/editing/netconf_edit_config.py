"""NETCONF edit config."""
from typing import Optional

from ncclient.manager import Manager
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import RpcResult, check_capability


def netconf_edit_config(
    task: Task,
    config: str,
    target: Optional[str] = "running",
    manager: Optional[Manager] = None,
    default_operation: Optional[str] = "merge",
) -> Result:
    """Edit configuration of the device using Netconf.

    Arguments:
        config (str): Configuration snippet to apply
        target (str): Target configuration store
        manager (Manager): NETCONF Manager
        default_operation (str): merge or replace

    Examples:
        Simple example::

            > nr.run(task=netconf_edit_config, config=desired_config)

        Changing Default Operation::

            > nr.run(task=netconf_edit_config, config=desired_config, default_operation="replace")

        Changing Default Target of `running` to `candidate`::

            > nr.run(task=netconf_edit_config, target="candidate", config=desired_config, default_operation="replace")

    Returns:
        Result object with the following attributes set::

            * result (RpcResult): Rpc and Manager
    """
    if default_operation not in ["merge", "replace"]:
        raise ValueError(f"{default_operation} not supported.")
    if not manager:
        manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    if target in ["candidate", "startup"]:
        capabilities = list(manager.server_capabilities)
        if not check_capability(capabilities, target):
            raise ValueError(f"{target} datastore is not supported.")
    result = manager.edit_config(config, target=target, default_operation=default_operation)

    result = RpcResult(rpc=result, manager=manager)
    return Result(host=task.host, result=result)
