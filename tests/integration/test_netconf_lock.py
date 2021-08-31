from nornir_netconf.plugins.tasks import netconf_lock


def test_netconf_lock(nornir):
    """Test Netconf Lock."""
    nr = nornir.filter(name="netconf1")
    result = nr.run(netconf_lock, datastore="candidate")

    assert result["netconf1"].result["ok"]
    assert not result["netconf1"].result["errors"]


def test_netconf_lock_failed(nornir):
    """Test Netconf Lock - failed."""
    nr = nornir.filter(name="netconf1")
    result = nr.run(netconf_lock, datastore="candidate")
    assert result["netconf1"].failed
    assert "already locked by this session" in str(result["netconf1"].result["error"])
