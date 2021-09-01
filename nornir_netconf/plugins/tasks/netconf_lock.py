"""NETCONF lock."""
from ncclient.operations.rpc import RPCError
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import get_result


def netconf_lock(task: Task, datastore: str) -> Result:
    """Lock a specified datastore.

    Arguments:
        datastore: Datastore to lock

    Examples:
        Simple example::

            > nr.run(task=netconf_lock)

        Locking candidate datestore::

            > nr.run(task=netconf_lock,
            >        datastore="candidate")

    Returns:
        Result object with the following attributes set:
          * unpack_rpc (``dict``):
    """
    result = {"failed": False, "result": {}}

    manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)

    # Wrapping in try/block as it's possible the lock doesn't work at times.
    # However, the keys stay true to match "get_result" helper function.

    try:
        result = manager.lock(target=datastore)
    except RPCError as err_ex:
        result["error"] = err_ex
        result["failed"] = True

    # Return the manager as part of the result. This can be used to pass into
    # other functions, if a global lock is in place. Typically, you can extract
    # session, session_id and use it.

    result_dict = get_result(result)
    result_dict["result"]["manager"] = manager
    return Result(host=task.host, **result_dict)
