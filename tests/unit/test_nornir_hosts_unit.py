"""Test inventory DEVICE_NAMEs."""


def test_netconf_device_name(nornir):
    nr = nornir.filter(name="ceos")
    assert "ceos" in nr.inventory.hosts
