from nornir_netconf.plugins.tasks import netconf_get


def test_netconf_get(nornir):
    nr = nornir.filter(name="netconf1.no_group")
    assert nr.inventory.hosts

    result = nr.run(netconf_get)

    assert result.items()
    for _, v in result.items():
        assert "<?xml version=" in v.result


def test_netconf_get_subtree(nornir):
    nr = nornir.filter(name="netconf1.no_group")
    assert nr.inventory.hosts

    result = nr.run(
        netconf_get,
        path="<netconf-server><listen></listen></netconf-server>",
        filter_type="subtree",
    )

    assert result.items()
    for _, v in result.items():
        assert "<listen" in v.result
