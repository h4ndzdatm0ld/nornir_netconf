"""Test NETCONF edit-config unit test."""
from unittest.mock import MagicMock, patch

from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import netconf_edit_config
from tests.conftest import FakeRpcObject

HOST = "nokia_rtr"


@patch("ncclient.manager.connect_ssh")
def test_netconf_edit_config_success(ssh, nornir, sros_config_payload):
    """Test NETCONF edit-config, no defined manager."""
    response_rpc = MagicMock()
    response = MagicMock()
    response.server_capabilities = ["netconf:capability:candidate"]
    response.edit_config.return_value = response_rpc
    ssh.return_value = response

    nr = nornir.filter(name=HOST)
    result = nr.run(netconf_edit_config, target="running", config=sros_config_payload)
    assert not result[HOST].failed
    assert result[HOST].result.rpc.ok


@patch("ncclient.manager.connect_ssh")
def test_netconf_edit_config_manager_set(ssh, nornir, sros_config_payload):
    """Test NETCONF edit-config, with manager option set."""
    # Create Fake RPC Object class. Set 'ok' attr to True.
    response_rpc = MagicMock()
    manager = MagicMock()
    manager.server_capabilities = ["netconf:capability:candidate"]
    manager.edit_config.return_value = response_rpc

    nr = nornir.filter(name=HOST)
    result = nr.run(netconf_edit_config, target="candidate", config=sros_config_payload, manager=manager)
    assert not result[HOST].failed
    assert result[HOST].result.rpc.ok


@patch("ncclient.manager.connect_ssh")
def test_netconf_edit_config_bad_operation(ssh, nornir, sros_config_payload):
    """Test NETCONF edit-config, unsupported default operation."""
    response_rpc = MagicMock(0)
    response = MagicMock()
    response.edit_config.return_value = response_rpc
    ssh.return_value = response

    nr = nornir.filter(name=HOST)
    result = nr.run(netconf_edit_config, target="candidate", config=sros_config_payload, default_operation="MARGE")
    assert result[HOST].failed


@patch("ncclient.manager.connect_ssh")
def test_netconf_edit_config_success_running(ssh, nornir, sros_config_payload):
    """Test NETCONF edit-config, no defined manager, no candidate."""
    response_rpc = MagicMock()
    response_rpc.set_ok(set=True)
    response = MagicMock()
    response.edit_config.return_value = response_rpc
    ssh.return_value = response

    nr = nornir.filter(name=HOST)
    result = nr.run(netconf_edit_config, target="running", config=sros_config_payload)
    assert not result[HOST].failed
    assert result[HOST].result.rpc.ok


@patch("ncclient.manager.connect_ssh")
def test_netconf_edit_config_no_capability(ssh, nornir, sros_config_payload):
    """Test NETCONF edit-config, candidate not supported."""
    # Create Fake RPC Object class. Set 'ok' attr to True.
    response_rpc = FakeRpcObject()
    response_rpc.set_ok(set=False)
    # Create a Mock Object. Assign 'edit-config' method and response
    # as the Fake RPC Object.
    response = MagicMock()
    response.server_capabilities = ["netconf:capability:validate:"]
    response.edit_config.return_value = response_rpc
    ssh.return_value = response

    nr = nornir.filter(name=HOST)
    result = nr.run(netconf_edit_config, target="startup", config=sros_config_payload)
    assert result[HOST].failed
    print_result(result)
