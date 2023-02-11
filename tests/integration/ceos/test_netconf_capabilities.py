"""Test NETCONF capabilities."""
from nornir_netconf.plugins.tasks import netconf_capabilities

CAP = "http://openconfig.net/yang/policy-forwarding?module=openconfig-policy-forwarding&revision=2021-08-06"


def test_netconf_capabilities(nornir):
    """Test NETCONF Capabilities."""
    nr = nornir.filter(vendor="arista")
    result = nr.run(netconf_capabilities)
    print(result)

    assert not result.failed
    for host in ["ceos_rtr_1", "ceos_rtr_2"]:
        assert CAP in result[host][0].result
        assert CAP in result[host][0].result
