"""NETCONF lock."""
from typing import Optional

from ncclient.manager import Manager
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import RpcResult


def netconf_lock(
    task: Task,
    datastore: Optional[str] = "candidate",
    manager: Optional[Manager] = None,
    operation: str = "lock",
) -> Result:
    """NETCONF locking operations for a specified datastore.

    By default, netconf_lock operations will display the 'data_xml'
    extracted from the RPCReply of the server, as it should be mininal
    data to display unlike other operations.

    Task name dynamically updated based on operation.

    Arguments:
        datastore (str): Datastore to lock
        manager (Manager): Manager to use if operation=='unlock'
        operation (str): Unlock or Lock

    Examples:
        Simple example::

            > nr.run(task=netconf_lock)

        Lock candidate datestore::

            > nr.run(task=netconf_lock,
            >        operation="lock",
            >        datastore="candidate")

        Unlock candidate datestore::

            > nr.run(task=netconf_lock,
            >        operation="unlock",
            >        datastore="candidate")

    Returns:
        Result object
    """
    operation = operation.strip().lower()
    if operation not in ["lock", "unlock"]:
        raise ValueError("Supported operations are: 'lock' or 'unlock'.")
    if not manager:
        manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    if operation == "lock":
        result = manager.lock(target=datastore)
    else:
        result = manager.unlock(target=datastore)
        task.name = "netconf_unlock"

    result = RpcResult(manager=manager, rpc=result)
    return Result(host=task.host, result=result)
