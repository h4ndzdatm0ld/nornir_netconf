"""Integration test against SROS device."""
# from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import netconf_get
from tests.conftest import CONFIGS_DIR, skip_integration_tests, xml_dict

DEVICE_NAME = "nokia_rtr"


@skip_integration_tests
def test_sros_netconf_get(nornir):
    """Test NETCONF get operation."""
    nr = nornir.filter(name=DEVICE_NAME)
    filter = """
    <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
        <card>
            <slot-number>1</slot-number>
        </card>
    </state>
    """

    result = nr.run(netconf_get, filter_type="subtree", path=filter)
    with open(f"{CONFIGS_DIR}/{DEVICE_NAME}-router-get.xml", "w+") as file:
        file.write(result[DEVICE_NAME].result.rpc.data_xml)
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    assert result[DEVICE_NAME].result
    assert (
        "85f24527c381450e926892441835ad7f"
        == parsed["rpc-reply"]["data"]["state"]["card"]["hardware-data"]["part-number"]
    )
    assert "state" in list(parsed["rpc-reply"]["data"].keys())
