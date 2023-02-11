"""Test NETCONF get."""
from nornir_netconf.plugins.tasks import netconf_get


def test_netconf_get(nornir):
    """Test NETCONF get operation."""
    nr = nornir.filter(name="netconf_sysrepo")
    result = nr.run(netconf_get)

    assert result["netconf_sysrepo"].result["ok"]
    # assert (
    #     "netconf-start-time"
    #     in result["netconf_sysrepo"].result["xml_dict"]["data"]["netconf-state"]["statistics"].keys()
    # )


def test_netconf_get_subtree(nornir):
    """Test NETCONF get with subtree."""
    nr = nornir.filter(name="netconf_sysrepo")

    result = nr.run(netconf_get, path="<netconf-server><listen></listen></netconf-server>", filter_type="subtree")
    assert result["netconf_sysrepo"].result["ok"]
    # assert "netconf-server" in result["netconf_sysrepo"].result["xml_dict"]["data"].keys()
