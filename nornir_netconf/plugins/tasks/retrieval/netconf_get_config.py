"""NETCONF get config."""
from typing import Any, Dict, Optional

from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import RpcResult


#  - > Prob don't need to add defaults.
def netconf_get_config(
    task: Task, source: Optional[str] = "running", path: Optional[str] = "", filter_type: Optional[str] = "xpath"
) -> Result:
    """Get configuration over Netconf from device.

    Arguments:
        source: Configuration store to collect from
        path: Subtree or xpath to filter
        filter_type: Type of filtering to use, 'xpath' or 'subtree'

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
    params: Dict[str, Any] = {"source": source}
    if path:
        params["filter"] = (filter_type, path)
    result = manager.get_config(**params)

    result = RpcResult(rpc=result, manager=manager)
    return Result(host=task.host, result=result)
