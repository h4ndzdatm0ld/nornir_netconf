"""Test NETCONF lock - integration."""
from typing import List

import pytest
from ncclient.manager import Manager
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result

# from nornir.core.filter import F
from nornir_netconf.plugins.tasks import netconf_lock
from tests.conftest import skip_integration_tests

GROUP_NAME = "integration"


def eval_multi_result(hosts: List, result: Result) -> None:
    """Repeatable multi host common test operation."""
    print_result(result)
    assert set(hosts) == set(list(result.keys()))
    for host in hosts:
        if hasattr(result[host].result.rpc, "ok"):
            assert result[host].result.rpc.ok
        assert not result[host].failed


def eval_multi_task_result(hosts: List, result: Result) -> None:
    """Repeatable multi host common test operation when running multi tasks."""
    print_result(result)
    assert set(hosts) == set(list(result.keys()))
    for host in hosts:
        for task in range(len(result[host])):
            assert not result[host][task].failed


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


def global_lock(task, datastore: str, operation: str, manager: Manager = None):
    """Test global lock operation of 'running' datastore."""
    if operation == "unlock":
        manager = task.host["manager"]
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
