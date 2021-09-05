"""NETCONF get."""
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import get_result


def netconf_get(task: Task, path: str = "", filter_type: str = "xpath", xmldict: bool = False) -> Result:
    """Get information over Netconf from device.

    Arguments:
        path: Subtree or xpath to filter
        filter_type: Type of filtering to use, 'xpath' or 'subtree'
        xmldict (boolean): convert xml to dict

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

    manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)

    if path:
        params["filter"] = (filter_type, path)
    result = manager.get(**params)
    return Result(host=task.host, **get_result(result, xmldict))
