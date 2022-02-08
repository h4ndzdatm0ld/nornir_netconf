"""Test NETCONF Commit.

Testing against netconf_sysrepo, fully patched but there is a small bug with patching
that conflicts with patching SSH on the next set of tests for edit_config.
Context manager doesn't help, but using a different host does.
"""
from nornir_netconf.plugins.tasks import netconf_commit
from unittest.mock import patch, MagicMock
from tests.conftest import FakeRpcObject


@patch("ncclient.manager.connect_ssh")
def test_netconf_commit_success(ssh, nornir):
    """Test success."""
    # Create Fake RPC Object class. Set 'ok' attr to True.
    response_rpc = FakeRpcObject()
    response_rpc.set_ok(set=True)
    # Create a Mock Object. Assign 'commit' method and response
    # as the Fake RPC Object.
    response = MagicMock()
    response.commit.return_value = response_rpc
    # Set the SSH session to return the FakeRPC Object when
    # performing edit-config call.
    ssh.return_value = response
    # Run Nornir
    nr = nornir.filter(name="netconf_sysrepo")
    result = nr.run(netconf_commit)
    assert not result["netconf_sysrepo"].failed
    assert not result["netconf_sysrepo"].result["error"]
    assert not result["netconf_sysrepo"].result["errors"]
    assert result["netconf_sysrepo"].result["rpc"]


@patch("ncclient.manager.connect_ssh")
def test_netconf_commit_success_with_manager(ssh, nornir):
    """Test success with manager."""
    # Create Fake RPC Object class. Set 'ok' attr to True.
    response_rpc = FakeRpcObject()
    response_rpc.set_ok(set=True)
    # Create a Mock Object. Assign 'commit' method and response
    # as the Fake RPC Object.
    manager = MagicMock()
    manager.commit.return_value = response_rpc
    # Run Nornir
    nr = nornir.filter(name="netconf2")
    result = nr.run(netconf_commit, manager=manager)
    assert not result["netconf2"].failed
    assert not result["netconf2"].result["error"]
    assert not result["netconf2"].result["errors"]
    assert result["netconf2"].result["rpc"]
    ssh.reset_mock()
