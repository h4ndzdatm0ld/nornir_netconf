"""Test inventory DEVICE_NAMEs."""


def test_netconf_DEVICE_NAMEs(nornir):
    nr = nornir.filter(name="ceos")
    assert "ceos" in nr.inventory.DEVICE_NAMEs
