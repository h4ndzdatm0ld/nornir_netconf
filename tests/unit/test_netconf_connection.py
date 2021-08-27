import os

from nornir_netconf.plugins.tasks import netconf_capabilities

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def test_netconf_connection_non_existent_ssh_config(nornir):
    nr = nornir.filter(name="netconf2.no_group")
    assert nr.inventory.hosts

    nr.config.ssh.config_file = "i dont exist"
    result = nr.run(netconf_capabilities)
    assert result

    for _, v in result.items():
        assert not isinstance(v.exception, FileNotFoundError)


def test_netconf_connection_ssh_config_exists(nornir):
    nr = nornir.filter(name="netconf2.no_group")

    assert nr.inventory.hosts

    nr.config.ssh.config_file = f"{DIR_PATH}/inventory_data/ssh_config"
    result = nr.run(netconf_capabilities)
    assert result

    for _, v in result.items():
        assert not isinstance(v.exception, FileNotFoundError)
