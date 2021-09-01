"""Integration test against SROS device."""
from nornir_netconf.plugins.tasks import (
    netconf_capabilities,
    netconf_edit_config,
    netconf_get,
    netconf_get_config,
    netconf_lock,
)
from nornir_utils.plugins.functions import print_result
from tests.conftest import skip_integration_tests

DEVICE_NAME = "nokia_rtr"


CONFIG = """
<config>
    <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
        <router>
            <router-name>Base</router-name>
            <interface>
                <interface-name>L3-OAM-eNodeB069420-W1</interface-name>
                <admin-state>disable</admin-state>
                <ingress-stats>false</ingress-stats>
            </interface>
        </router>
    </configure>
</config>
"""


@skip_integration_tests
def test_sros_netconf_edit_config(nornir):
    """Test NETCONF edit-config."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_edit_config, config=CONFIG, target="candidate")
    assert result


@skip_integration_tests
def test_sros_netconf_capabilities(nornir):
    """Test NETCONF Capabilities."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_capabilities)
    assert "urn:ietf:params:netconf:base:1.0" in result[DEVICE_NAME].result


@skip_integration_tests
def test_sros_netconf_get_config(nornir):
    """Test get config."""
    nr = nornir.filter(name=DEVICE_NAME)

    result = nr.run(
        netconf_get_config,
        source="running",
        path="""
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <router>
                <router-name>Base</router-name>
            </router>
        </configure>
        """,
        filter_type="subtree",
    )
    assert result
    print_result(result)
    # with open("tests/unit/test_data/get-sros-config.xml", "w+") as file:
    #     file.write(result[DEVICE_NAME].result["rpc"].data_xml)


@skip_integration_tests
def test_sros_netconf_get(nornir):
    """Test NETCONF get operation."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_get)
    assert result[DEVICE_NAME].result["ok"]
    assert result[DEVICE_NAME].result


@skip_integration_tests
def test_sros_netconf_lock(nornir):
    """Test Netconf Lock."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_lock, datastore="candidate")

    assert result[DEVICE_NAME].result["ok"]
