from nornir_netconf.plugins.tasks import netconf_capabilities


def test_netconf_capabilities(nornir):
    nr = nornir.filter(name="netconf1.no_group")
    assert nr.inventory.hosts

    result = nr.run(netconf_capabilities)

    assert result.items()
    for _, v in result.items():
        assert "urn:ietf:params:netconf:capability:writable-running:1.0" in v.result
