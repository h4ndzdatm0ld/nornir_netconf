from nornir_netconf.plugins.tasks import netconf_lock

# from nornir_utils.plugins.functions import print_result


def test_netconf_lock(nornir):
    """Test Netconf Lock."""
    nr = nornir.filter(name="netconf1")
    result = nr.run(netconf_lock, datastore="candidate")

    assert result["netconf1"].result["ok"]
    assert not result["netconf1"].result["errors"]
