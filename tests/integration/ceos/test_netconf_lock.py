"""Test NETCONF lock - integration."""
from ncclient.manager import Manager
from ncclient.operations.rpc import RPCReply

from nornir_netconf.plugins.helpers import RpcResult
from nornir_netconf.plugins.tasks import netconf_lock


def test_netconf_lock(nornir):
    """Test Netconf Lock."""
    nr = nornir.filter(name="netconf_sysrepo")
    result = nr.run(netconf_lock, datastore="candidate", operation="lock")
    assert result["netconf_sysrepo"].result.rpc.ok
    assert isinstance(result["netconf_sysrepo"].result, RpcResult)
    assert isinstance(result["netconf_sysrepo"].result.manager, Manager)
    assert isinstance(result["netconf_sysrepo"].result.rpc, RPCReply)


def test_netconf_lock_failed(nornir):
    """Test Netconf Lock - failed."""
    nr = nornir.filter(name="netconf_sysrepo")
    result = nr.run(netconf_lock, datastore="candidate", operation="lock")
    assert result["netconf_sysrepo"].failed
    assert (
        str(result["netconf_sysrepo"].result.error)
        == "Access to the requested lock is denied because the lock is currently held by another entity."
    )
    assert isinstance(result["netconf_sysrepo"].result.manager, Manager)
    assert isinstance(result["netconf_sysrepo"].result, RpcResult)
