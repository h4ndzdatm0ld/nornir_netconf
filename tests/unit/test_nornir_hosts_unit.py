"""Test inventory hosts."""


def test_netconf_hosts(nornir):
    nr = nornir.filter(name="ceos")
    assert "ceos" in nr.inventory.hosts
