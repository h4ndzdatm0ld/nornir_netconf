"""Integration test against IOSXE device."""

# from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import netconf_get
from tests.conftest import skip_integration_tests, xml_dict

DEVICE_NAME = "iosxe_rtr"


@skip_integration_tests
def test_iosxe_netconf_get(nornir):
    """Test NETCONF get operation."""
    nr = nornir.filter(name=DEVICE_NAME)
    filter = """
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
            <domain></domain>
        </ip>
    </native>
    """
    result = nr.run(netconf_get, filter_type="subtree", path=filter)
    parsed = xml_dict(result[DEVICE_NAME].result.rpc)

    assert result[DEVICE_NAME].result
    assert parsed["rpc-reply"]["data"]["native"]["ip"]["domain"]["name"] == "example.com"
