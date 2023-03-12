"""Integration test against SROS device."""
from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import (
    netconf_commit,
    netconf_edit_config,
    netconf_get,
    netconf_get_config,
)
from tests.conftest import skip_integration_tests

DEVICE_NAME = "nokia_rtr"


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
    assert result[DEVICE_NAME].result.rpc
    assert result[DEVICE_NAME].result.rpc.data_xml
    # with open("tests/test_data/get-sros-config.xml", "w+") as file:
    #     file.write(result[DEVICE_NAME].result.rpc.data_xml)


@skip_integration_tests
def test_sros_netconf_get(nornir):
    """Test NETCONF get operation."""
    nr = nornir.filter(name=DEVICE_NAME)
    filter = """
    <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
        <python/>
    </configure>
    """
    result = nr.run(netconf_get, filter_type="subtree", path=filter)
    assert result[DEVICE_NAME].result
    assert result[DEVICE_NAME].result.rpc.data_xml


@skip_integration_tests
def test_sros_netconf_edit_config(nornir, sros_config_payload):
    """Test NETCONF edit-config - Post Lock / Unlock operations."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_edit_config, config=sros_config_payload, target="candidate")
    # assert "ok/" in result[DEVICE_NAME].result.rpc.data_xml
    print_result(result)

    # Commit Config
    commit = nr.run(netconf_commit)
    assert commit.result.rpc.ok
