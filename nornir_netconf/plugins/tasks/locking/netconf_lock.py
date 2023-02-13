"""NETCONF lock."""
from ncclient.manager import Manager
from ncclient.operations.rpc import RPCError
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import RpcResult


def netconf_lock(task: Task, datastore: str, manager: Manager = None, operation: str = "lock") -> Result:
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

        lock candidate datestore::

            > nr.run(task=netconf_lock,
            >        operation="lock",
            >        datastore="candidate")

    Returns:
        Result object with the following attributes set:
          * unpack_rpc (``dict``):
    """
    failed = False
    error = None

    operation = operation.strip().lower()
    if operation not in ["lock", "unlock"]:
        failed = True
        raise ValueError("Supported operations are: 'lock' or 'unlock'.")
    if not manager:
        manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    try:
        if operation == "lock":
            result = manager.lock(target=datastore)
        else:
            result = manager.unlock(target=datastore)
            task.name = "netconf_unlock"
    except RPCError as err_ex:
        error = err_ex
        failed = True

    # Return the manager as part of the result. This can be used to pass into
    # other functions, if a global lock is in place. Typically, you can extract
    # session, session_id and use it.

    rpc_result = RpcResult(
        xml=result.xml if hasattr(result, "xml") else getattr(result, "data_xml", None),
        rpc=manager,
        error=error,
        errors=result.errors if hasattr(result, "errors") else None,
    )
    return Result(host=task.host, failed=failed, result=rpc_result)
