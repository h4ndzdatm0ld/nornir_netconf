"""Integration test against IOSXE device."""

# from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import netconf_get_config
from tests.conftest import CONFIGS_DIR, skip_integration_tests, xml_dict

DEVICE_NAME = "iosxe_rtr"


@skip_integration_tests
def test_iosxe_netconf_get_config(nornir):
    """Test NETCONF get config."""
    nr = nornir.filter(name=DEVICE_NAME)

    result = nr.run(
        netconf_get_config,
        source="running",
        path="""
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>GigabitEthernet1</name>
            </interface>
        </interfaces>
        """,
        filter_type="subtree",
    )

    assert result[DEVICE_NAME].result.rpc
    assert result[DEVICE_NAME].result.rpc.data_xml
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    assert "10.0.0.15" == parsed["data"]["interfaces"]["interface"]["ipv4"]["address"]["ip"]

    with open(f"{CONFIGS_DIR}/iosxe-interface-gigabitethernet1.xml", "w+") as file:
        file.write(result[DEVICE_NAME].result.rpc.data_xml)


@skip_integration_tests
def test_iosxe_netconf_get_full_config(nornir):
    """Test NETCONF get full config."""
    nr = nornir.filter(name=DEVICE_NAME)

    result = nr.run(
        netconf_get_config,
        source="running",
    )
    assert result[DEVICE_NAME].result.rpc
    assert result[DEVICE_NAME].result.rpc.data_xml
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    assert "vr-csr-1" == parsed["data"]["native"]["hostname"]
    with open(f"{CONFIGS_DIR}/iosxe-full-config.xml", "w+") as file:
        file.write(result[DEVICE_NAME].result.rpc.data_xml)
