from nornir_netconf.plugins.tasks import netconf_get_config


def test_netconf_get_config(nornir):
    """Test get config."""
    nr = nornir.filter(name="netconf_sysrepo")

    result = nr.run(netconf_get_config, source="startup")
    assert result["netconf_sysrepo"].result["ok"]
    # assert (
    #     result["netconf_sysrepo"].result["xml_dict"]["data"]["keystore"]["asymmetric-keys"]["asymmetric-key"]["name"]
    #     == "genkey"
    # )


def test_netconf_get_config_running(nornir):
    """Test get running config as default."""
    nr = nornir.filter(name="netconf_sysrepo")

    result = nr.run(netconf_get_config)
    assert result["netconf_sysrepo"].result["ok"]
    # assert (
    #     result["netconf_sysrepo"].result["xml_dict"]["data"]["netconf-server"]["listen"]["endpoint"]["name"]
    #     == "default-ssh"
    # )


def test_netconf_get_config_subtree(nornir):
    """Test filter subtree of get_config."""
    nr = nornir.filter(name="netconf_sysrepo")
    assert nr.inventory.hosts

    result = nr.run(
        netconf_get_config,
        source="startup",
        path="<keystore xmlns='urn:ietf:params:xml:ns:yang:ietf-keystore'><asymmetric-keys><asymmetric-key><name></name></asymmetric-key></asymmetric-keys></keystore>",
        filter_type="subtree",
    )
    assert result["netconf_sysrepo"].result["ok"]
    # assert "keystore" in result["netconf_sysrepo"].result["xml_dict"]["data"].keys()
    # assert "netconf-server" not in result["netconf_sysrepo"].result["xml_dict"]["data"].keys()
