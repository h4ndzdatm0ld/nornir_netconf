"""Integration test against IOSXR device."""
from nornir_netconf.plugins.tasks import netconf_get_config
from tests.conftest import CONFIGS_DIR, skip_integration_tests, xml_dict

DEVICE_NAME = "iosxr_rtr"


@skip_integration_tests
def test_iosxr_netconf_get_config(nornir):
    """Test NETCONF get config."""
    nr = nornir.filter(name=DEVICE_NAME)

    result = nr.run(
        netconf_get_config,
        source="running",
        path="""
        <interfaces xmlns="http://openconfig.net/yang/interfaces">
        </interfaces>
        """,
        filter_type="subtree",
    )
    assert result[DEVICE_NAME].result.rpc
    assert result[DEVICE_NAME].result.rpc.data_xml
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    assert "MgmtEth0/0/CPU0/0" == parsed["data"]["interfaces"]["interface"][0]["name"]

    with open(f"{CONFIGS_DIR}/iosxr-interfaces.xml", "w+") as file:
        file.write(result[DEVICE_NAME].result.rpc.data_xml)
