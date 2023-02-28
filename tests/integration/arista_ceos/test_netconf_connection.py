"""Test NETCONF Connection."""
import os

from nornir_netconf.plugins.tasks import netconf_capabilities

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DEVICE_NAME = "ceos"
CAP = "http://openconfig.net/yang/policy-forwarding?module=openconfig-policy-forwarding&revision=2021-08-06"


def test_netconf_connection_missing_ssh_keyfile(nornir):
    """Test netconf connection - no ssh config file."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_capabilities)

    assert isinstance(result[DEVICE_NAME].result, list)


def test_netconf_connection_non_existent_ssh_config(nornir):
    """Test netconf connection - bad ssh config path."""
    nr = nornir.filter(name=DEVICE_NAME)
    nr.config.ssh.config_file = "i dont exist"
    result = nr.run(netconf_capabilities)
    assert nr.config.ssh.config_file == "i dont exist"
    assert isinstance(result[DEVICE_NAME].result, list)
    assert CAP in result[DEVICE_NAME].result


def test_netconf_connection_ssh_config_exists(nornir):
    nr = nornir.filter(name=DEVICE_NAME)
    nr.config.ssh.config_file = f"{DIR_PATH}/inventory_data/ssh_config"
    result = nr.run(netconf_capabilities)

    assert isinstance(result[DEVICE_NAME].result, list)
    assert CAP in result[DEVICE_NAME].result


def test_netconf_connection_ssh_keyfile(nornir):
    """Test netconf connection - with shh config file."""
    nr = nornir.filter(name="ceos_empty_ssh_file")
    result = nr.run(netconf_capabilities)
    assert isinstance(result["ceos_empty_ssh_file"].result, list)
