"""Test NETCONF rpc unit test."""
from unittest.mock import MagicMock, patch

from nornir_netconf.plugins.tasks import netconf_rpc

# from nornir_utils.plugins.functions import print_result


DEVICE_NAME = "nokia_rtr"


@patch("ncclient.manager.connect_ssh")
def test_netconf_rpc_success(ssh, nornir, sros_rpc_payload):
    """Test NETCONF rpc, no defined manager."""
    response_rpc = MagicMock()
    response = MagicMock()
    response.rpc.return_value = response_rpc
    ssh.return_value = response

    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_rpc, payload=sros_rpc_payload)
    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc.ok


@patch("ncclient.manager.connect_ssh")
def test_netconf_rpc_success_action(ssh, nornir, sros_rpc_payload_action):
    """Test NETCONF rpc action (namespace set), no defined manager."""
    response_rpc = MagicMock()
    response = MagicMock()
    response.rpc.return_value = response_rpc
    ssh.return_value = response

    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_rpc, payload=sros_rpc_payload_action)
    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc.ok


@patch("ncclient.manager.connect_ssh")
def test_netconf_rpc_manager_set(ssh, nornir, sros_rpc_payload):
    """Test NETCONF rpc, with manager option set."""
    response_rpc = MagicMock()
    manager = MagicMock()
    manager.rpc.return_value = response_rpc

    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_rpc, payload=sros_rpc_payload, manager=manager)
    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc.ok


@patch("ncclient.manager.connect_ssh")
def test_netconf_rpc_bad_operation(ssh, nornir, sros_rpc_payload):
    """Test NETCONF rpc, unsupported default operation."""
    response_rpc = MagicMock(0)
    response = MagicMock()
    response.rpc.return_value = response_rpc
    ssh.return_value = response

    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_rpc, payload=sros_rpc_payload, default_operation="MARGE")
    assert result[DEVICE_NAME].failed
