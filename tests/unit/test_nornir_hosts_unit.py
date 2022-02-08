"""Test inventory hosts."""


def test_netconf_hosts(nornir):
    nr = nornir.filter(name="netconf_sysrepo")
    assert "netconf_sysrepo" in nr.inventory.hosts
