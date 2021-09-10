"""Test NETCONF lock - integration."""
from nornir_netconf.plugins.tasks import netconf_lock


def test_netconf_lock(nornir):
    """Test Netconf Lock."""
    nr = nornir.filter(name="netconf1")
    result = nr.run(netconf_lock, datastore="candidate", operation="lock")
    assert result["netconf1"].result["ok"]
    assert not result["netconf1"].result["errors"]
    assert not result["netconf1"].result["error"]
    assert result["netconf1"].result["manager"]
    assert result["netconf1"].result["rpc"]


def test_netconf_lock_failed(nornir):
    """Test Netconf Lock - failed."""
    nr = nornir.filter(name="netconf1")
    result = nr.run(netconf_lock, datastore="candidate", operation="lock")
    assert result["netconf1"].failed
    assert "already locked by this session" in str(result["netconf1"].result["error"])
    assert "Unable to find 'ok' or data_xml in response object." in result["netconf1"].result["errors"]
    assert not result["netconf1"].result["ok"]
    assert not result["netconf1"].result["rpc"]
    assert not result["netconf1"].result["xml_dict"]
