"""Test NETCONF lock - integration."""
from ncclient.manager import Manager
from ncclient.operations.rpc import RPCReply

from nornir_netconf.plugins.helpers import RpcResult
from nornir_netconf.plugins.tasks import netconf_lock

DEVICE_NAME = "ceos"


def test_netconf_lock(nornir):
    """Test Netconf Lock."""
    nr = nornir.filter(name=HOST)
    result = nr.run(netconf_lock, datastore="running", operation="lock")
    assert result[HOST].result.rpc.ok
    assert isinstance(result[HOST].result, RpcResult)
    assert isinstance(result[HOST].result.manager, Manager)
    assert isinstance(result[HOST].result.rpc, RPCReply)


def test_netconf_lock_failed(nornir):
    """Test Netconf Lock - failed."""
    nr = nornir.filter(name=HOST)
    result = nr.run(netconf_lock, datastore="running", operation="lock")
    assert result[HOST].failed
