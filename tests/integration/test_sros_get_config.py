"""Integration test against SROS device."""
from nornir_netconf.plugins.tasks import netconf_get_config
from tests.conftest import skip_integration_tests


@skip_integration_tests
def test_netconf_get_config_sros(nornir):
    """Test get config."""
    nr = nornir.filter(name="nokia_rtr")

    result = nr.run(netconf_get_config)
    assert result
