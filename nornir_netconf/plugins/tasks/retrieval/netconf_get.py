"""NETCONF get."""
from ncclient.operations.rpc import RPCError
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME


def netconf_get(task: Task, path: str = "", filter_type: str = "xpath") -> Result:
    """Get information over Netconf from device.

    Arguments:
        path: Subtree or xpath to filter
        filter_type: Type of filtering to use, 'xpath' or 'subtree'

    Examples:
        Simple example::

            > nr.run(task=netconf_get)

        Passing options using ``xpath``::

            > query = "/devices/device"
            > nr.run(task=netconf_get,
            >        path=query)

       Passing options using ``subtree``::

            > query = "<interfaces></interfaces>"
            > nr.run(task=netconf_get,
            >        filter_type="subtree",
            >        path=query)


    Returns:
        Result object with the following attributes set:
          * result (``str``): The collected data as an XML string
    """
    params = {}
    error = None
    result = None

    if path:
        params["filter"] = (filter_type, path)

    try:
        manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
        result = manager.get(**params)
    except RPCError as rpc_error:
        error = rpc_error

    result = RpcResult(rpc=result, manager=manager, error=error)
    return Result(host=task.host, result=result)
