"""Test NETCONF validate unit test."""
from unittest.mock import MagicMock, patch

from nornir_netconf.plugins.tasks import netconf_validate

DEVICE_NAME = "nokia_rtr"


@patch("ncclient.manager.connect_ssh")
def test_netconf_netconf_validate_success(ssh, nornir):
    """Test NETCONF netconf_validate, no defined manager."""
    response_rpc = MagicMock()
    response = MagicMock()
    response.validate.return_value = response_rpc

    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_validate, source="running")
    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc.ok


@patch("ncclient.manager.connect_ssh")
def test_netconf_validate_manager_set(ssh, nornir):
    """Test NETCONF edit-config, with manager option set."""
    response_rpc = MagicMock()
    manager = MagicMock()
    manager.validate.return_value = response_rpc

    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_validate, source="candidate", manager=manager)
    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc.ok
