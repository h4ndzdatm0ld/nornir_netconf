"""NETCONF lock."""
from ncclient.manager import Manager
from ncclient.operations.rpc import RPCError
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import get_result


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
    result = {"failed": False, "result": {}}

    operation = operation.strip().lower()
    if operation not in ["lock", "unlock"]:
        result["failed"] = True
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
        result["error"] = err_ex
        result["failed"] = True

    # Return the manager as part of the result. This can be used to pass into
    # other functions, if a global lock is in place. Typically, you can extract
    # session, session_id and use it.

    result_dict = get_result(result)
    result_dict["result"]["manager"] = manager

    # Handle different responses & Update results
    options = dir(result)
    if "data_xml" in options:
        result_dict["result"]["data_xml"] = result.data_xml  # type: ignore
    elif "xml" in options:
        result_dict["result"]["data_xml"] = result.xml  # type: ignore
    else:
        result_dict["result"]["data_xml"] = None
    return Result(host=task.host, **result_dict)
