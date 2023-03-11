"""Integration test against IOSXR device."""
from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import (
    netconf_capabilities,
    netconf_commit,
    netconf_edit_config,
    netconf_get,
    netconf_get_config,
)
from tests.conftest import skip_integration_tests

DEVICE_NAME = "iosxr_rtr"


@skip_integration_tests
def test_iosxr_netconf_capabilities(nornir):
    """Test NETCONF Capabilities."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_capabilities)
    assert any(cap for cap in result[DEVICE_NAME].result if "http://cisco.com/ns/yang/cisco-xr-ietf" in cap)


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
    # assert "MgmtEth0/0/CPU0/0" == result[DEVICE_NAME].result["xml_dict"]["data"]["interfaces"]["interface"][0]["name"]
    assert result[DEVICE_NAME].result.rpc
    assert result[DEVICE_NAME].result.rpc.data_xml
    # with open("tests/test_data/get-iosxr-config.xml", "w+") as file:
    # file.write(result[DEVICE_NAME].result.rpc.data_xml)


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
    # assert result[DEVICE_NAME].result["xml_dict"]["data"]["interfaces"]["interface"]["config"]["enabled"]


@skip_integration_tests
def test_iosxr_netconf_edit_config(nornir, iosxr_config_payload):
    """Test NETCONF edit-config - Post Lock / Unlock operations."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_edit_config, config=iosxr_config_payload, target="candidate")
    assert result[DEVICE_NAME].result.rpc.ok

    # print_result(result)

    # Commit Config
    result = nr.run(netconf_commit)
    assert result[DEVICE_NAME].result.rpc.ok
    print_result(result)
