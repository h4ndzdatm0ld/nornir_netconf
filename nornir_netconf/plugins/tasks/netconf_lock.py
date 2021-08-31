"""NETCONF lock."""
from ncclient.operations.rpc import RPCError
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import unpack_rpc


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
        result["result"] = unpack_rpc(manager.lock(target=datastore))
    except RPCError as err_ex:
        result["failed"] = True
        result["result"]["error"] = err_ex

    return Result(host=task.host, **result)
