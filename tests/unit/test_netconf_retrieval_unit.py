"""Unit tests for NETCONF retrieval tasks and connection cleanup."""

from unittest.mock import MagicMock, patch

from nornir_netconf.plugins.connections.netconf import Netconf
from nornir_netconf.plugins.tasks import (
    netconf_capabilities,
    netconf_get,
    netconf_get_config,
)

DEVICE_NAME = "ceos"


@patch("ncclient.manager.connect_ssh")
def test_netconf_capabilities(connect_ssh, nornir):
    """Return the server capabilities and the manager that supplied them."""
    manager = MagicMock()
    manager.server_capabilities = ["urn:ietf:params:netconf:base:1.0"]
    connect_ssh.return_value = manager

    result = nornir.filter(name=DEVICE_NAME).run(task=netconf_capabilities)

    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc == manager.server_capabilities
    assert result[DEVICE_NAME].result.manager is manager


@patch("ncclient.manager.connect_ssh")
def test_netconf_get_without_filter(connect_ssh, nornir):
    """Issue an unfiltered get request."""
    manager = MagicMock()
    reply = MagicMock()
    manager.get.return_value = reply
    connect_ssh.return_value = manager

    result = nornir.filter(name=DEVICE_NAME).run(task=netconf_get)

    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc is reply
    manager.get.assert_called_once_with()


@patch("ncclient.manager.connect_ssh")
def test_netconf_get_with_filter(connect_ssh, nornir):
    """Forward the requested NETCONF filter."""
    manager = MagicMock()
    reply = MagicMock()
    manager.get.return_value = reply
    connect_ssh.return_value = manager

    result = nornir.filter(name=DEVICE_NAME).run(
        task=netconf_get,
        path="/interfaces",
        filter_type="xpath",
    )

    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc is reply
    manager.get.assert_called_once_with(filter=("xpath", "/interfaces"))


@patch("ncclient.manager.connect_ssh")
def test_netconf_get_config_without_filter(connect_ssh, nornir):
    """Issue an unfiltered running datastore request."""
    manager = MagicMock()
    reply = MagicMock()
    manager.get_config.return_value = reply
    connect_ssh.return_value = manager

    result = nornir.filter(name=DEVICE_NAME).run(task=netconf_get_config)

    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc is reply
    manager.get_config.assert_called_once_with(source="running")


@patch("ncclient.manager.connect_ssh")
def test_netconf_get_config_with_filter(connect_ssh, nornir):
    """Forward the source and requested NETCONF filter."""
    manager = MagicMock()
    reply = MagicMock()
    manager.get_config.return_value = reply
    connect_ssh.return_value = manager

    result = nornir.filter(name=DEVICE_NAME).run(
        task=netconf_get_config,
        source="candidate",
        path="<interfaces/>",
        filter_type="subtree",
    )

    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.rpc is reply
    manager.get_config.assert_called_once_with(
        source="candidate",
        filter=("subtree", "<interfaces/>"),
    )


def test_netconf_close():
    """Close the underlying ncclient session."""
    connection = MagicMock()
    plugin = Netconf()
    plugin.connection = connection

    plugin.close()

    connection.close_session.assert_called_once_with()


@patch("ncclient.manager.connect_ssh")
def test_netconf_open_with_ssh_config(connect_ssh, tmp_path):
    """Forward an existing SSH configuration file to ncclient."""
    ssh_config = tmp_path / "ssh_config"
    ssh_config.write_text("Host *\n")
    configuration = MagicMock()
    plugin = Netconf()

    plugin.open(
        hostname="192.0.2.1",
        username="admin",
        password="secret",
        platform="default",
        extras={"ssh_config": str(ssh_config)},
        configuration=configuration,
    )

    connect_ssh.assert_called_once_with(
        host="192.0.2.1",
        username="admin",
        password="secret",
        port=830,
        device_params={"name": "default"},
        ssh_config=str(ssh_config),
    )
