"""NETCONF commit."""
from typing import Optional

from ncclient.manager import Manager
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers.rpc_helpers import get_result


def netconf_commit(
    task: Task,
    manager: Optional[Manager] = None,
    xmldict: bool = False,
    confirmed: bool = False,
    timeout: int = 60,
    persist: int = None,  # type: ignore
    persist_id: int = None,  # type: ignore
) -> Result:
    """Commit operation.

    Arguments:
        manager: class:: ncclient.manager.Manager
        xmldict (boolean): convert xml to dict
        confirmed (boolean): Commit confirm
        timeout (int): commit confirm timeout
        persist (int): survive a session termination
        persist_id (int): must equal given value of persist in original commit operation
    Examples:
        Simple example::

            > nr.run(task=netconf_commit, manager=manager)

    Returns:
        Result object with the following attributes set:
          * result (``str``): The rpc-reply as an XML string
    """
    if not manager:
        manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    result = manager.commit(confirmed, timeout, persist, persist_id)
    return Result(host=task.host, **get_result(result, xmldict))
