"""Test NETCONF lock - integration."""
from ncclient.manager import Manager
from ncclient.operations.rpc import RPCReply

from nornir_netconf.plugins.helpers import RpcResult
from nornir_netconf.plugins.tasks import netconf_lock

DEVICE_NAME = "ceos"


def test_netconf_lock(nornir):
    """Test Netconf Lock."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_lock, datastore="running", operation="lock")
    assert result[DEVICE_NAME].result.rpc.ok
    assert isinstance(result[DEVICE_NAME].result, RpcResult)
    assert isinstance(result[DEVICE_NAME].result.manager, Manager)
    assert isinstance(result[DEVICE_NAME].result.rpc, RPCReply)


def test_netconf_lock_failed(nornir):
    """Test Netconf Lock - failed."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_lock, datastore="running", operation="lock")
    assert result[DEVICE_NAME].failed
    result = nr.run(netconf_lock, datastore="running", operation="unlock")
