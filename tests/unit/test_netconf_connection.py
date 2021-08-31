"""Test NETCONF Connection."""
import os

from nornir_netconf.plugins.tasks import netconf_capabilities

from nornir_utils.plugins.functions import print_result

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def test_netconf_connection_non_existent_ssh_config_none(nornir):
    """Test netconf connection - no ssh config file."""
    nr = nornir.filter(name="netconf3")

    nr.config.ssh.config_file = None
    result = nr.run(netconf_capabilities)
    print_result(result)


# def test_netconf_connection_non_existent_ssh_config(nornir):
#     """Test netconf connection - no ssh config file."""
#     nr = nornir.filter(name="netconf1")

#     nr.config.ssh.config_file = "i dont exist"
#     result = nr.run(netconf_capabilities)
#     assert nr.config.ssh.config_file == "i dont exist"
#     for _, v in result.items():
#         assert not isinstance(v.exception, FileNotFoundError)


# def test_netconf_connection_ssh_config_exists(nornir):
#     nr = nornir.filter(name="netconf1")

#     nr.config.ssh.config_file = f"{DIR_PATH}/inventory_data/ssh_config"
#     result = nr.run(netconf_capabilities)
#     assert result

#     for _, v in result.items():
#         assert not isinstance(v.exception, FileNotFoundError)
