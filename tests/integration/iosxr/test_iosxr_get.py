"""Integration test against IOSXR device."""
from nornir_netconf.plugins.tasks import netconf_get
from tests.conftest import skip_integration_tests, xml_dict

DEVICE_NAME = "iosxr_rtr"


@skip_integration_tests
def test_iosxr_netconf_get(nornir):
    """Test NETCONF get operation."""
    nr = nornir.filter(name=DEVICE_NAME)
    filter = """
    <interfaces xmlns="http://openconfig.net/yang/interfaces">
        <interface>
            <name>MgmtEth0/0/CPU0/0</name>
        </interface>
    </interfaces>
    """
    result = nr.run(netconf_get, filter_type="subtree", path=filter)
    assert result[DEVICE_NAME].result
    assert result[DEVICE_NAME].result.rpc.data_xml
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    assert "true" == parsed["data"]["interfaces"]["interface"]["state"]["enabled"]
