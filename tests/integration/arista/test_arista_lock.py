"""Test NETCONF lock - integration."""

from ncclient.manager import Manager
from ncclient.operations.rpc import RPCReply

from nornir_netconf.plugins.helpers import RpcResult
from nornir_netconf.plugins.tasks import netconf_lock

# from nornir_utils.plugins.functions import print_result


DEVICE_NAME = "ceos"


def test_netconf_lock(nornir):
    """Test Netconf Lock."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_lock, datastore="candidate", operation="lock")
    assert result[DEVICE_NAME].result.rpc.ok
    assert isinstance(result[DEVICE_NAME].result, RpcResult)
    assert isinstance(result[DEVICE_NAME].result.manager, Manager)
    assert isinstance(result[DEVICE_NAME].result.rpc, RPCReply)
    result = nr.run(netconf_lock, datastore="candidate", operation="unlock")
    assert result[DEVICE_NAME].result.rpc.ok


# TODO: Fix this test
# def test_netconf_lock_failed(nornir):
#     """Test Netconf Lock - failed."""
#     nr = nornir.filter(name=DEVICE_NAME)
#     lock_operation = nr.run(netconf_lock, datastore="candidate", operation="lock")
#     assert lock_operation[DEVICE_NAME].result.rpc.ok
#     failed_lock = nr.run(netconf_lock, datastore="candidate", operation="lock")
#     assert failed_lock[DEVICE_NAME].failed
