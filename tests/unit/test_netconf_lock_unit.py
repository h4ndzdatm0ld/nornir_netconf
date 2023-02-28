"""Test NETCONF Lock - unit-tests."""
from unittest.mock import MagicMock, patch

from nornir_netconf.plugins.tasks import netconf_lock

DEVICE_NAME = "ceos"


def test_netconf_lock(nornir):
    """Test Netconf Lock, operation not found."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_lock, datastore="candidate", operation="kock")
    assert result[DEVICE_NAME].failed


@patch("ncclient.manager.Manager")
@patch("ncclient.manager.connect_ssh")
def test_netconf_lock_strip_lower(ssh, manager, nornir):
    """Test Netconf Lock, operation lock success."""
    response_rpc = MagicMock()
    manager.lock.return_value = response_rpc
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_lock, datastore="candidate", operation=" Lock", manager=manager)
    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc


@patch("ncclient.manager.Manager")
@patch("ncclient.manager.connect_ssh")
def test_netconf_with_manager(ssh, manager, nornir):
    """Test Netconf Lock, custom manager."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_lock, datastore="candidate", operation=" LOCK ", manager=manager)
    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc
