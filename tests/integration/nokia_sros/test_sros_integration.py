"""Integration test against SROS device."""
from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import (
    netconf_capabilities,
    netconf_commit,
    netconf_edit_config,
    netconf_get,
    netconf_get_config,
    netconf_lock,
)
from tests.conftest import skip_integration_tests

DEVICE_NAME = "nokia_rtr"


@skip_integration_tests
def test_sros_netconf_capabilities(nornir):
    """Test NETCONF Capabilities."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_capabilities)
    # print_result(result)
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
def test_sros_netconf_lock_operations(nornir, sros_config_payload):
    """Test NETCONF Lock, extract manager and use it to edit-config.

    Afterwards, use netconf_lock with unlock operations to unlock.
    """
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_lock, datastore="candidate", operation="lock")
    manager = result[DEVICE_NAME].result.manager
    assert result[DEVICE_NAME].result.rpc
    assert result[DEVICE_NAME].result.manager
    assert result[DEVICE_NAME].result["data_xml"]
    # Extract manager from lock operation.
    manager = result[DEVICE_NAME].result.manager
    # print_result(result)

    # Edit Config
    result = nr.run(netconf_edit_config, config=sros_config_payload, target="candidate", manager=manager)
    # print_result(result)
    assert not result[DEVICE_NAME].result["error"]
    assert not result[DEVICE_NAME].result["errors"]
    assert "ok/" in result[DEVICE_NAME].result.rpc.data_xml
    # assert "ok" in result[DEVICE_NAME].result["xml_dict"]["rpc-reply"].keys()

    # Commit Config
    result = nr.run(netconf_commit, manager=manager)
    # print_result(result)
    assert not result[DEVICE_NAME].result["error"]
    assert not result[DEVICE_NAME].result["errors"]
    assert "ok/" in result[DEVICE_NAME].result.rpc.data_xml
    # assert "ok" in result[DEVICE_NAME].result["xml_dict"]["rpc-reply"].keys()

    # Unlock candidate datastore.
    result = nr.run(netconf_lock, datastore="candidate", operation="unlock", manager=manager)
    assert result[DEVICE_NAME].result.rpc
    assert result[DEVICE_NAME].result.manager
    assert result[DEVICE_NAME].result["data_xml"]
    # print_result(result)


@skip_integration_tests
def test_sros_netconf_edit_config(nornir, sros_config_payload):
    """Test NETCONF edit-config - Post Lock / Unlock operations."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_edit_config, config=sros_config_payload, target="candidate")
    assert not result[DEVICE_NAME].result["errors"]
    assert "ok/" in result[DEVICE_NAME].result.rpc.data_xml
    # assert not result[DEVICE_NAME].result["xml_dict"]["rpc-reply"]["ok"]
    print_result(result)

    # Commit Config
    result = nr.run(netconf_commit)
    # assert "ok" in result[DEVICE_NAME].result["xml_dict"]["rpc-reply"].keys()
