"""Integration test against IOSXE device."""
from nornir_netconf.plugins.tasks import netconf_capabilities
from tests.conftest import skip_integration_tests

DEVICE_NAME = "iosxe_rtr"


@skip_integration_tests
def test_iosxe_netconf_capabilities(nornir):
    """Test NETCONF Capabilities."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_capabilities)
    assert any(cap for cap in result[DEVICE_NAME].result if "cisco-xe-openconfig-acl-deviation" in cap)
