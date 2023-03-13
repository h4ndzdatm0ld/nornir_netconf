"""Conftest for nornir_netconf UnitTests."""
import os
import shutil
import time
from distutils.util import strtobool
from typing import Any, Dict, List

import pytest
import xmltodict
from nornir import InitNornir
from nornir.core.state import GlobalState
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result

# pytest mark decorator to skip integration tests if INTEGRATION_TESTS=True
# These tests will connect to local lab environment to validate actual responses
# from locallly hosted network devices.
skip_integration_tests = pytest.mark.skipif(
    bool(strtobool(os.environ.get("RUN_INTEGRATION_TESTS", "False"))),
    reason="Integration tests require virtual devices running.",
)

global_data = GlobalState(dry_run=True)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIGS_DIR = f"{DIR_PATH}/test_data/configs"

# If NORNIR_LOG set to True, the log won't be deleted in teardown.
nornir_logfile = os.environ.get("NORNIR_LOG", False)


@pytest.fixture()
def nornir():
    """Initializes nornir"""
    nornir = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": f"{DIR_PATH}/inventory_data/hosts.yml",
                "group_file": f"{DIR_PATH}/inventory_data/groups.yml",
                "defaults_file": f"{DIR_PATH}/inventory_data/defaults.yml",
            },
        },
        logging={"log_file": f"{DIR_PATH}/test_data/nornir_test.log", "level": "DEBUG"},
        dry_run=True,
    )
    nornir.data = global_data
    return nornir


@pytest.fixture(scope="session", autouse=True)
def schema_path():
    """Schema path, test data."""
    return f"{DIR_PATH}/test_data/schemas"


@pytest.fixture(scope="session", autouse=True)
def test_folder():
    """Test folder."""
    return "tests/test_data/test_folder"


@pytest.fixture(scope="module", autouse=True)
def teardown_class(schema_path, test_folder):
    """Teardown the random artifacts created by pytesting."""
    if not nornir_logfile:
        nornir_log = f"{DIR_PATH}/test_data/nornir_test.log"
        if os.path.exists(nornir_log):
            os.remove(nornir_log)

    # Remove test data folders
    folders = [test_folder, schema_path]
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)


@pytest.fixture(scope="function", autouse=True)
def reset_data():
    """Reset Data."""
    global_data.dry_run = True
    global_data.reset_failed_hosts()


# PAYLOADS


@pytest.fixture(scope="function", autouse=True)
def sros_config_payload():
    return """
<config>
    <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
        <router>
            <router-name>Base</router-name>
            <interface>
                <interface-name>L3-OAM-eNodeB069420-W1</interface-name>
                <admin-state>disable</admin-state>
                <ingress-stats>false</ingress-stats>
            </interface>
        </router>
    </configure>
</config>
        """


def xml_dict(xml: str) -> Dict[str, Any]:
    """Convert XML to Dict.

    Args:
        xml (str): XML string

    Returns:
        Dict: XML converted to Dict
    """
    return xmltodict.parse(str(xml))


def eval_multi_task_result(hosts: List, result: Result) -> None:
    """Repeatable multi host common test operation when running multi tasks."""
    print_result(result)
    assert set(hosts) == set(list(result.keys()))
    for host in hosts:
        for task in range(len(result[host])):
            assert not result[host][task].failed


def eval_multi_result(hosts: List, result: Result) -> None:
    """Repeatable multi host common test operation."""
    print_result(result)
    assert set(hosts) == set(list(result.keys()))
    for host in hosts:
        if hasattr(result[host].result.rpc, "ok"):
            assert result[host].result.rpc.ok
        assert not result[host].failed


@pytest.fixture(autouse=True, scope="module")
def slow_down_tests():
    yield
    time.sleep(3)
