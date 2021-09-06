"""Test NETCONF capabilities."""
from nornir_netconf.plugins.tasks import netconf_capabilities

# from nornir_utils.plugins.functions import print_result


def test_netconf_capabilities(nornir):
    """Test NETCONF Capabilities."""
    nr = nornir.filter(name="netconf1")
    result = nr.run(netconf_capabilities)
    # print_result(result)
    assert result.items()
    for _, v in result.items():
        assert "urn:ietf:params:netconf:capability:writable-running:1.0" in v.result
