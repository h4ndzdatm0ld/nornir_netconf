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
    failed = False
    result = {}
    manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)

    try:
        result = unpack_rpc(manager.lock(target=datastore))
    except RPCError as err_ex:
        failed = True
        result["error"] = err_ex

    return Result(host=task.host, failed=failed, result=result)
