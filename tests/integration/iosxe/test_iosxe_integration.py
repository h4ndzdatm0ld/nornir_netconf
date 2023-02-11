"""Integration test against IOSXR device."""
# from nornir_utils.plugins.functions import print_result
from nornir_netconf.plugins.tasks import (
    netconf_capabilities,
    netconf_get,
    netconf_get_config,
)
from tests.conftest import skip_integration_tests

DEVICE_NAME = "iosxe_rtr"


@skip_integration_tests
def test_iosxe_netconf_capabilities(nornir):
    """Test NETCONF Capabilities."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_capabilities)
    assert any(cap for cap in result[DEVICE_NAME].result if "cisco-xe-openconfig-acl-deviation" in cap)


@skip_integration_tests
def test_iosxe_netconf_get_config(nornir):
    """Test NETCONF get config."""
    nr = nornir.filter(name=DEVICE_NAME)

    result = nr.run(
        netconf_get_config,
        source="running",
        path="""
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <banner>
                <motd>
                </motd>
            </banner>
        </native>
        """,
        filter_type="subtree",
    )
    # assert (
    #     "Welcome to the DevNet Sandbox"
    #     in result[DEVICE_NAME].result["xml_dict"]["data"]["native"]["banner"]["motd"]["banner"]
    # )
    assert result[DEVICE_NAME].result["rpc"]
    assert result[DEVICE_NAME].result["rpc"].data_xml
    # with open("tests/test_data/get-iosxe-config-filter.xml", "w+") as file:
    #     file.write(result[DEVICE_NAME].result["rpc"].data_xml)


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
    assert result[DEVICE_NAME].result
    # assert result[DEVICE_NAME].result["xml_dict"]["data"]["native"]["ip"]["domain"]["name"] == "lab.devnetsandbox.local"
