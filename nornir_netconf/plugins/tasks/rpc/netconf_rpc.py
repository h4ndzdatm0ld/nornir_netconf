"""NETCONF rpc generic call."""
from typing import Optional

from ncclient import xml_
from ncclient.manager import Manager
from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME
from nornir_netconf.plugins.helpers import RpcResult


def netconf_rpc(
    task: Task,
    payload: str,
    manager: Optional[Manager] = None,
) -> Result:
    """This method is a "bare-bones" rpc call which does not apply any
    formatting/standardization beyond the outer most rpc tag.

    Arguments:
        payload (str): Payload snippet to apply
        manager (Manager): NETCONF Manager

    Examples:
        Simple example::
            > desired_payload='<save-config xmlns="http://cisco.com/yang/cisco-ia"/>'
            > nr.run(task= netconf_rpc, payload=desired_payload)


    Returns:
        Result object with the following attributes set::

            * result (RpcResult): Rpc and Manager
    """
    if not manager:
        manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    result = manager.rpc(xml_.to_ele(payload))

    result = RpcResult(rpc=result, manager=manager)
    return Result(host=task.host, result=result)
