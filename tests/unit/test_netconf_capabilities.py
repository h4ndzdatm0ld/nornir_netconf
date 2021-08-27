from nornir_netconf.plugins.tasks import netconf_capabilities


def test_netconf_capabilities(nornir):
    nr = nornir.filter(name="netconf3")
    assert nr.inventory.hosts

    result = nr.run(netconf_capabilities)

    assert result.items()
    for _, v in result.items():
        print(v.result)
        assert "urn:ietf:params:netconf:capability:writable-running:1.0" in v.result
