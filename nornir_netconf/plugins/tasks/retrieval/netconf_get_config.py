"""NETCONF get config."""
from typing import Any, Dict

from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers.rpc_helpers import get_result


def netconf_get_config(
    task: Task, source: str = "running", path: str = "", filter_type: str = "xpath", xmldict: bool = False
) -> Result:
    """Get configuration over Netconf from device.

    Arguments:
        source: Configuration store to collect from
        path: Subtree or xpath to filter
        filter_type: Type of filtering to use, 'xpath' or 'subtree'
        xmldict (boolean): convert xml to dict

    Examples:
        Simple example::

            > nr.run(task=netconf_get_config)

        Collect startup config::

            > nr.run(task=netconf_get_config, source="startup")


        Passing options using ``xpath``::

            > xpath = "/devices/device"
            > nr.run(task=netconf_get_config,
            >        path=xpath)

        Passing options using ``subtree``::

            > subtree = "<interfaces></interface>"
            > nr.run(task=netconf_get_config,
            >        filter_type="subtree",
            >        path=subtree)


    Returns:
        Result object with the following attributes set:
          * result (``str``): The collected data as an XML string
    """
    manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    parameters: Dict[str, Any] = {"source": source}

    if path:
        parameters["filter"] = (filter_type, path)

    result = manager.get_config(**parameters)
    return Result(host=task.host, **get_result(result, xmldict))
