from nornir_netconf.plugins.tasks import netconf_get_config


def test_netconf_get_config(nornir):
    nr = nornir.filter(name="netconf1.no_group")
    assert nr.inventory.hosts

    result = nr.run(netconf_get_config, source="startup")

    for _, v in result.items():
        assert "<turing-machine" in v.result


def test_netconf_get_config_subtree(nornir):
    nr = nornir.filter(name="netconf1.no_group")
    assert nr.inventory.hosts

    result = nr.run(
        netconf_get_config,
        source="startup",
        path="<interfaces></interfaces>",
        filter_type="subtree",
    )

    for _, v in result.items():
        assert "<interface" in v.result
