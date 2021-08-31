"""Test inventory hosts."""


def test_netconf_hosts(nornir):
    nr = nornir.filter(name="netconf1")
    assert "netconf1" in nr.inventory.hosts
