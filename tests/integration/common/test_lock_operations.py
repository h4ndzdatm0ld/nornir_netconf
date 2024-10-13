"""Test NETCONF lock - integration."""

import pytest

from nornir_netconf.plugins.tasks import netconf_lock
from tests.conftest import (
    eval_multi_result,
    eval_multi_task_result,
    skip_integration_tests,
)

GROUP_NAME = "integration"


@skip_integration_tests
@pytest.mark.parametrize(
    "datastore, expected_hosts", [("running", ["ceos", "iosxe_rtr"]), ("candidate", ["iosxr_rtr", "nokia_rtr"])]
)
def test_netconf_lock_and_unlock_datastore(nornir, datastore, expected_hosts):
    """Test Netconf Lock and Unlock with manager carrying."""
    nr = nornir.filter(lock_datastore=datastore)
    result = nr.run(netconf_lock, datastore=datastore, operation="lock")
    eval_multi_result(expected_hosts, result)
    result = nr.run(netconf_lock, datastore=datastore, operation="unlock")
    assert set(expected_hosts) == set(list(result.keys()))
    eval_multi_result(expected_hosts, result)


def global_lock(task, datastore: str, operation: str):
    """Test global lock operation of 'running' datastore."""
    if operation == "unlock":
        manager = task.host["manager"]
        print(manager)
    else:
        manager = None
    result = task.run(netconf_lock, datastore=datastore, operation=operation, manager=manager)
    task.host["manager"] = result.result.manager
    if hasattr(result.result.rpc, "ok"):
        assert result.result.rpc.ok
    assert not result.failed


@skip_integration_tests
@pytest.mark.parametrize(
    "datastore, expected_hosts", [("running", ["ceos", "iosxe_rtr"]), ("candidate", ["iosxr_rtr", "nokia_rtr"])]
)
def test_netconf_global_lock(datastore, expected_hosts, nornir):
    """Test Netconf Lock and Unlock with carried manager session."""
    nr = nornir.filter(lock_datastore=datastore)
    result = nr.run(global_lock, datastore=datastore, operation="lock")
    eval_multi_task_result(expected_hosts, result)
    result = nr.run(global_lock, datastore=datastore, operation="unlock")
    eval_multi_task_result(expected_hosts, result)


@skip_integration_tests
@pytest.mark.parametrize(
    "datastore, expected_hosts", [("running", ["ceos", "iosxe_rtr"]), ("candidate", ["iosxr_rtr", "nokia_rtr"])]
)
def test_netconf_lock_lock_failed(datastore, expected_hosts, nornir):
    """Test Netconf Lock and attempting second lock - failed."""
    nr = nornir.filter(lock_datastore=datastore)
    result = nr.run(global_lock, datastore=datastore, operation="lock")
    eval_multi_task_result(expected_hosts, result)
    result = nr.run(global_lock, datastore=datastore, operation="lock")
    assert set(expected_hosts) == set(list(result.keys()))
    for host in expected_hosts:
        for task in range(len(result[host])):
            assert result[host][task].failed
    result = nr.run(global_lock, datastore=datastore, operation="unlock")
