"""Test NETCONF Lock - unit-tests."""
from nornir_netconf.plugins.tasks import netconf_lock
from unittest.mock import patch
from tests.conftest import FakeRpcObject

# from nornir_utils.plugins.functions import print_result


def test_netconf_lock(nornir):
    """Test Netconf Lock, operation not found."""
    nr = nornir.filter(name="netconf1")
    result = nr.run(netconf_lock, datastore="candidate", operation="kock")
    assert result["netconf1"].failed


@patch("ncclient.manager.Manager")
@patch("ncclient.manager.connect_ssh")
def test_netconf_lock_strip_lower(ssh, manager, nornir):
    """Test Netconf Lock, operation lock success."""
    response_rpc = FakeRpcObject()
    response_rpc.set_ok(set=True)
    manager.lock.return_value = response_rpc

    nr = nornir.filter(name="netconf1")
    result = nr.run(netconf_lock, datastore="candidate", operation=" Lock", manager=manager)
    assert not result["netconf1"].failed
    assert result["netconf1"].result["manager"]


@patch("ncclient.manager.Manager")
@patch("ncclient.manager.connect_ssh")
def test_netconf_with_manager(ssh, manager, nornir):
    """Test Netconf Lock, custom manager."""
    nr = nornir.filter(name="netconf1")
    result = nr.run(netconf_lock, datastore="candidate", operation=" Lock", manager=manager)
    assert result["netconf1"].failed
    assert result["netconf1"].result["manager"]


@patch("ncclient.manager.Manager")
@patch("ncclient.manager.connect_ssh")
def test_netconf_unlock(ssh, manager, nornir):
    """Test Netconf Lock, custom manager + data_xml."""
    response_rpc = FakeRpcObject()
    response_rpc.set_ok(set=True)
    manager.unlock.return_value = response_rpc

    nr = nornir.filter(name="netconf1")
    result = nr.run(netconf_lock, datastore="candidate", operation="unlock", manager=manager)
    assert not result["netconf1"].failed
    assert "netconf_unlock" in str(result["netconf1"])
    assert result["netconf1"].result["manager"]
    assert result["netconf1"].result["ok"]
    assert not result["netconf1"].result["data_xml"]  # data_xml found in fake_rpc_obj
