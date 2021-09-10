"""Test NETCONF edit-config unit test."""
from unittest.mock import MagicMock, patch

from nornir_netconf.plugins.tasks import netconf_edit_config
from tests.conftest import FakeRpcObject

# from nornir_utils.plugins.functions import print_result


@patch("ncclient.manager.connect_ssh")
def test_netconf_edit_config_success(ssh, nornir, sros_config_payload):
    """Test NETCONF edit-config, no defined manager."""
    # Create Fake RPC Object class. Set 'ok' attr to True.
    response_rpc = FakeRpcObject()
    response_rpc.set_ok(set=True)
    # Create a Mock Object. Assign 'edit-config' method and response
    # as the Fake RPC Object.
    response = MagicMock()
    response.edit_config.return_value = response_rpc
    ssh.return_value = response

    nr = nornir.filter(name="netconf2")
    result = nr.run(netconf_edit_config, target="candidate", config=sros_config_payload)
    assert not result["netconf2"].failed
    assert result["netconf2"].result["ok"]
    assert not result["netconf2"].result["error"]
    assert not result["netconf2"].result["errors"]
    assert result["netconf2"].result["rpc"]


@patch("ncclient.manager.connect_ssh")
def test_netconf_edit_config_manager_set(ssh, nornir, sros_config_payload):
    """Test NETCONF edit-config, with manager option set."""
    # Create Fake RPC Object class. Set 'ok' attr to True.
    response_rpc = FakeRpcObject()
    response_rpc.set_ok(set=True)
    # Create a Mock Object. Assign 'edit-config' method and response
    # as the Fake RPC Object.
    manager = MagicMock()
    manager.edit_config.return_value = response_rpc

    nr = nornir.filter(name="netconf1")
    result = nr.run(netconf_edit_config, target="candidate", config=sros_config_payload, manager=manager)
    assert not result["netconf1"].failed
    assert result["netconf1"].result["ok"]
    assert not result["netconf1"].result["error"]
    assert not result["netconf1"].result["errors"]
    assert result["netconf1"].result["rpc"]


@patch("ncclient.manager.connect_ssh")
def test_netconf_edit_config_bad_operation(ssh, nornir, sros_config_payload):
    """Test NETCONF edit-config, unsupported default operation."""
    # Create Fake RPC Object class. Set 'ok' attr to True.
    response_rpc = FakeRpcObject()
    response_rpc.set_ok(set=True)
    # Create a Mock Object. Assign 'edit-config' method and response
    # as the Fake RPC Object.
    response = MagicMock()
    response.edit_config.return_value = response_rpc
    ssh.return_value = response

    nr = nornir.filter(name="netconf2")
    result = nr.run(netconf_edit_config, target="candidate", config=sros_config_payload, default_operation="MARGE")
    # print_result(result)
    assert result["netconf2"].failed
