"""NETCONF edit config."""
from typing import Optional

from ncclient.manager import Manager
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers.rpc_helpers import get_result


def netconf_edit_config(
    task: Task, config: str, target: str = "running", manager: Optional[Manager] = None, xmldict: bool = False
) -> Result:
    """Edit configuration of device using Netconf.

    Arguments:
        config: Configuration snippet to apply
        target: Target configuration store
        manager: class:: ncclient.manager.Manager
        xmldict (boolean): convert xml to dict

    Examples:
        Simple example::

            > nr.run(task=netconf_edit_config, config=desired_config)

    Returns:
        Result object with the following attributes set:
          * result (``str``): The rpc-reply as an XML string
    """
    # Manager can come from locking a datastore, using 'netconf_lock'.
    if not manager:
        manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    result = manager.edit_config(config, target=target)
    return Result(host=task.host, **get_result(result, xmldict))
