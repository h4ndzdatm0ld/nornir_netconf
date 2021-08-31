"""Integration test against SROS device."""
from nornir_netconf.plugins.tasks import netconf_get_config, netconf_capabilities, netconf_get, netconf_lock
from tests.conftest import skip_integration_tests

DEVICE_NAME = "nokia_rtr"


@skip_integration_tests
def test_netconf_capabilities(nornir):
    """Test NETCONF Capabilities."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_capabilities)
    assert "urn:ietf:params:netconf:base:1.0" in result[DEVICE_NAME].result


@skip_integration_tests
def test_netconf_get_config_sros(nornir):
    """Test get config."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_get_config)
    assert result


@skip_integration_tests
def test_netconf_get(nornir):
    """Test NETCONF get operation."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_get)
    assert result[DEVICE_NAME].result["ok"]
    assert result[DEVICE_NAME].result


@skip_integration_tests
def test_netconf_lock(nornir):
    """Test Netconf Lock."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_lock, datastore="candidate")

    assert result[DEVICE_NAME].result["ok"]
