"""NETCONF lock."""
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import unpack_rpc


def netconf_lock(task: Task, datastore: str) -> Result:
    """Get information over Netconf from device.

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
    manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)

    result = manager.lock(target=datastore)

    if not result.ok:
        failed = True

    return Result(host=task.host, failed=failed, result=unpack_rpc(result))
