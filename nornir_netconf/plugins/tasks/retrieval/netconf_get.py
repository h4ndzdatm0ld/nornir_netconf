"""NETCONF get."""
from nornir.core.task import Optional, Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import RpcResult


def netconf_get(task: Task, path: Optional[str] = "", filter_type: Optional[str] = "xpath") -> Result:
    """Get configuration and state information over Netconf from device.

    Arguments:
        path (Optional[str]): `Subtree` or `xpath` to filter
        filter_type (Optional[str]): Type of filtering to use, `xpath or `subtree`

    Examples:
        Simple example::

            > nr.run(task=netconf_get)

        Passing options using ``xpath``::

            > xpath = "/devices/device"
            > nr.run(task=netconf_get,
            >        path=xpath)

        Passing options using ``subtree``::

            > subtree = "<interfaces></interfaces>"
            > nr.run(task=netconf_get,
            >        filter_type="subtree",
            >        path=subtree)


    Returns:
        Result object with the following attributes set::

            * result (RpcResult): Rpc and Manager
    """
    params = {}
    manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    if path:
        params["filter"] = (filter_type, path)
    result = manager.get(**params)

    result = RpcResult(rpc=result, manager=manager)
    return Result(host=task.host, result=result)
