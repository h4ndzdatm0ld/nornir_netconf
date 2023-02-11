"""Test NETCONF lock - integration."""
from nornir_netconf.plugins.tasks import netconf_lock


def test_netconf_lock(nornir):
    """Test Netconf Lock."""
    nr = nornir.filter(name="netconf_sysrepo")
    result = nr.run(netconf_lock, datastore="candidate", operation="lock")
    assert result["netconf_sysrepo"].result["ok"]
    assert not result["netconf_sysrepo"].result["errors"]
    assert not result["netconf_sysrepo"].result["error"]
    assert result["netconf_sysrepo"].result["manager"]
    assert result["netconf_sysrepo"].result["rpc"]


def test_netconf_lock_failed(nornir):
    """Test Netconf Lock - failed."""
    nr = nornir.filter(name="netconf_sysrepo")
    result = nr.run(netconf_lock, datastore="candidate", operation="lock")
    assert result["netconf_sysrepo"].failed
    assert str(result['netconf_sysrepo'].result['error']) == "Access to the requested lock is denied because the lock is currently held by another entity."
    # assert "Unable to find 'ok' or data_xml in response object." in result["netconf_sysrepo"].result["errors"]
    assert not result["netconf_sysrepo"].result["ok"]
    assert not result["netconf_sysrepo"].result["rpc"]

