"""Test NETCONF get."""
from nornir_netconf.plugins.tasks import netconf_get
from tests.conftest import xml_dict

DEVICE_NAME = "ceos"


def test_netconf_get(nornir):
    """Test NETCONF get operation."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_get)
    parsed = xml_dict(result[DEVICE_NAME].result.rpc)
    assert result[DEVICE_NAME].result.rpc.ok
    assert parsed["rpc-reply"]["data"]["system"]["config"]["hostname"] == "ceos"


def test_netconf_get_subtree(nornir):
    """Test NETCONF get with subtree.

    Subtree filter is used to get specific data from the device which returns a smaller RPC Reply.
    """
    nr = nornir.filter(name=DEVICE_NAME)

    path = "<acl><state></state></acl>"
    result = nr.run(netconf_get, path=path, filter_type="subtree")
    parsed = xml_dict(result[DEVICE_NAME].result.rpc)

    assert parsed["rpc-reply"]["data"]["acl"]["state"]["counter-capability"] == "AGGREGATE_ONLY"
