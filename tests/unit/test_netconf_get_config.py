from nornir_netconf.plugins.tasks import netconf_get_config


def test_netconf_get_config(nornir):
    nr = nornir.filter(name="netconf3.no_group")
    assert nr.inventory.hosts

    result = nr.run(netconf_get_config, source="startup")

    for _, v in result.items():
        print(v.result)
        assert "<name>genkey</name>" in v.result


def test_netconf_get_config_subtree(nornir):
    nr = nornir.filter(name="netconf3.no_group")
    assert nr.inventory.hosts

    result = nr.run(
        netconf_get_config,
        source="startup",
        path="<keystore xmlns='urn:ietf:params:xml:ns:yang:ietf-keystore'><asymmetric-keys><asymmetric-key><name></name></asymmetric-key></asymmetric-keys></keystore>",
        filter_type="subtree",
    )

    for _, v in result.items():
        assert "genkey" in v.result
