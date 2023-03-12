"""Integration test against SROS device."""
# from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import netconf_get_config
from tests.conftest import CONFIGS_DIR, skip_integration_tests, xml_dict

DEVICE_NAME = "nokia_rtr"


@skip_integration_tests
def test_sros_netconf_get_config(nornir):
    """Test get config with subtree."""
    nr = nornir.filter(name=DEVICE_NAME)

    result = nr.run(
        netconf_get_config,
        source="running",
        path="""
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <card></card>
        </configure>
        """,
        filter_type="subtree",
    )
    assert result[DEVICE_NAME].result.rpc
    assert result[DEVICE_NAME].result.rpc.data_xml
    with open(f"{CONFIGS_DIR}/{DEVICE_NAME}-xpath-router-config.xml", "w+") as file:
        file.write(result[DEVICE_NAME].result.rpc.data_xml)
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    assert "me12-100gb-qsfp28" == parsed["rpc-reply"]["data"]["configure"]["card"]["mda"][0]["mda-type"]


@skip_integration_tests
def test_sros_netconf_get_full_config(nornir):
    """Test get full config."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(
        netconf_get_config,
        source="running",
    )
    assert result[DEVICE_NAME].result.rpc
    assert result[DEVICE_NAME].result.rpc.data_xml
    assert not result[DEVICE_NAME].failed

    with open(f"{CONFIGS_DIR}/{DEVICE_NAME}-config.xml", "w+") as file:
        file.write(result[DEVICE_NAME].result.rpc.data_xml)
