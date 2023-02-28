"""Test NETCONF Commit.

that conflicts with patching SSH on the next set of tests for edit_config.
Context manager doesn't help, but using a different DEVICE_NAME does.
"""
from unittest.mock import MagicMock, patch

from nornir_netconf.plugins.helpers import RpcResult
from nornir_netconf.plugins.tasks import netconf_commit

DEVICE_NAME = "ceos"


@patch("ncclient.manager.connect_ssh")
def test_netconf_commit_success(ssh, nornir):
    """Test success."""
    response_rpc = MagicMock()
    response = MagicMock()
    response.commit.return_value = response_rpc
    ssh.return_value = response
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_commit)
    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc
    assert isinstance(result[DEVICE_NAME].result, RpcResult)


@patch("ncclient.manager.connect_ssh")
def test_netconf_commit_success_with_manager(ssh, nornir):
    """Test success with manager."""
    response_rpc = MagicMock()
    manager = MagicMock()
    manager.commit.return_value = response_rpc
    # Run Nornir
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_commit, manager=manager)
    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc
    ssh.reset_mock()
