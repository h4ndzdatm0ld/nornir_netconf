"""Test NETCONF get."""
from nornir_netconf.plugins.tasks import netconf_get
from tests.conftest import xml_dict

HOST = "ceos_rtr_1"


def test_netconf_get(nornir):
    """Test NETCONF get operation."""
    nr = nornir.filter(name=HOST)
    result = nr.run(netconf_get)
    parsed = xml_dict(result[HOST].result["rpc"])
    assert result[HOST].result["ok"]
    assert parsed["rpc-reply"]["data"]["system"]["config"]["hostname"] == "ceos1"
    # GET is used for `state` data
    assert (
        parsed["rpc-reply"]["data"]["components"]["component"][0]["state"]["type"]["#text"] == "oc-platform-types:CPU"
    )


def test_netconf_get_subtree(nornir):
    """Test NETCONF get with subtree.

    Subtree filter is used to get specific data from the device which returns a smaller RPC Reply.
    """
    nr = nornir.filter(name=HOST)

    path = "<acl><state></state></acl>"
    result = nr.run(netconf_get, path=path, filter_type="subtree")
    parsed = xml_dict(result[HOST].result["rpc"])

    assert parsed["rpc-reply"]["data"]["acl"]["state"]["counter-capability"] == "AGGREGATE_ONLY"
