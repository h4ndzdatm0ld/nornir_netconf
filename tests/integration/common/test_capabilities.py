"""Test NETCONF capabilities."""

from typing import Dict

from nornir.core.filter import F

from nornir_netconf.plugins.tasks import netconf_capabilities
from tests.conftest import eval_multi_task_result, skip_integration_tests

CEOS_EXPECTED_CAPABILITY = (
    "http://openconfig.net/yang/policy-forwarding?module=openconfig-policy-forwarding&revision=2021-08-06"
)
IOSXR_EXPECTED_CAPABILITY = (
    "http://cisco.com/ns/yang/Cisco-IOS-XR-es-acl-datatypes?module=Cisco-IOS-XR-es-acl-datatypes&revision=2015-11-09"
)
IOSXE_EXPECTED_CAPABILITY = (
    "http://cisco.com/ns/yang/Cisco-IOS-XE-device-tracking?module=Cisco-IOS-XE-device-tracking&revision=2020-03-01"
)
SROS_EXPECTED_CAPABILITY = "urn:nokia.com:sros:ns:yang:sr:types-rsvp?module=nokia-types-rsvp&revision=2018-02-08"


CAPABILITIES: Dict = {
    "ceos": CEOS_EXPECTED_CAPABILITY,
    "iosxe_rtr": IOSXE_EXPECTED_CAPABILITY,
    "nokia_rtr": SROS_EXPECTED_CAPABILITY,
    "iosxr_rtr": IOSXR_EXPECTED_CAPABILITY,
}


@skip_integration_tests
def test_netconf_capabilities(nornir):
    """Test NETCONF Capabilities."""
    nr = nornir.filter(F(groups__contains="integration"))
    hosts = list(nr.inventory.hosts.keys())
    result = nr.run(netconf_capabilities)
    eval_multi_task_result(hosts=hosts, result=result)
    for host in hosts:
        assert CAPABILITIES[host] in [cap for cap in result[host][0].result.rpc]
