"""Test NETCONF Connection."""
import os

from nornir_netconf.plugins.tasks import netconf_capabilities

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
HOST = "ceos"
CAP = "http://openconfig.net/yang/policy-forwarding?module=openconfig-policy-forwarding&revision=2021-08-06"


def test_netconf_connection_missing_ssh_keyfile(nornir):
    """Test netconf connection - no ssh config file."""
    nr = nornir.filter(name=HOST)
    result = nr.run(netconf_capabilities)
    assert isinstance(result[HOST].result, list)


def test_netconf_connection_non_existent_ssh_config(nornir):
    """Test netconf connection - bad ssh config path."""
    nr = nornir.filter(name=HOST)
    nr.config.ssh.config_file = "i dont exist"
    result = nr.run(netconf_capabilities)
    assert nr.config.ssh.config_file == "i dont exist"
    assert isinstance(result[HOST].result, list)
    assert CAP in result[HOST].result


def test_netconf_connection_ssh_config_exists(nornir):
    nr = nornir.filter(name=HOST)
    nr.config.ssh.config_file = f"{DIR_PATH}/inventory_data/ssh_config"
    result = nr.run(netconf_capabilities)

    assert isinstance(result[HOST].result, list)
    assert CAP in result[HOST].result


def test_netconf_connection_ssh_keyfile(nornir):
    """Test netconf connection - with shh config file."""
    nr = nornir.filter(name="netconf3")
    result = nr.run(netconf_capabilities)
    assert isinstance(result["netconf3"].result, list)


def test_netconf_connection_ssh_keyfile_null(nornir):
    """Test netconf connection - with null shh config file."""
    nr = nornir.filter(name="netconf4")
    result = nr.run(netconf_capabilities)
    assert isinstance(result["netconf4"].result, list)
