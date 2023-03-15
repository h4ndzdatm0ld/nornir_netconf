"""NETCONF commit."""
from typing import Optional

from ncclient.manager import Manager
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import RpcResult


def netconf_commit(
    task: Task,
    manager: Optional[Manager] = None,
    confirmed: Optional[bool] = False,
    timeout: Optional[int] = 60,
    persist: Optional[int] = None,
    persist_id: Optional[int] = None,
) -> Result:
    """Commit operation.

    Arguments:
        manager (Manager): NETCONF Manager
        confirmed (boolean): Commit confirm
        timeout (int): commit confirm timeout
        persist (int): survive a session termination
        persist_id (int): must equal given value of persist in original commit operation

    Examples:
        Simple example::

            > nr.run(task=netconf_commit)

        With a carried manager session::
            > nr.run(task=netconf_commit, manager=manager)

    Returns:
        Result object with the following attributes set::

            * result (RpcResult): Rpc and Manager
    """
    if not manager:
        manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    result = manager.commit(confirmed, timeout, persist, persist_id)
    result = RpcResult(rpc=result, manager=manager)
    return Result(host=task.host, result=result)
