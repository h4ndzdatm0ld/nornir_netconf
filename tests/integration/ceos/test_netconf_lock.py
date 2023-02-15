"""Test NETCONF lock - integration."""
from ncclient.manager import Manager

from nornir_netconf.plugins.tasks import netconf_lock


def test_netconf_lock(nornir):
    """Test Netconf Lock."""
    nr = nornir.filter(name="netconf_sysrepo")
    result = nr.run(netconf_lock, datastore="candidate", operation="lock")
    assert result["netconf_sysrepo"].result.ok
    assert not result["netconf_sysrepo"].result.errors
    assert not result["netconf_sysrepo"].result.error
    assert result["netconf_sysrepo"].result.rpc
    assert result["netconf_sysrepo"].result.xml
    # NETCONF Lock operations returns manager on `rpc` attribute
    assert isinstance(result["netconf_sysrepo"].result.rpc, Manager)


def test_netconf_lock_failed(nornir):
    """Test Netconf Lock - failed."""
    nr = nornir.filter(name="netconf_sysrepo")
    result = nr.run(netconf_lock, datastore="candidate", operation="lock")
    assert not result["netconf_sysrepo"].result.ok
    assert result["netconf_sysrepo"].failed
    assert (
        str(result["netconf_sysrepo"].result.error)
        == "Access to the requested lock is denied because the lock is currently held by another entity."
    )
    assert result["netconf_sysrepo"].result.rpc
    # NETCONF Lock operations returns manager on `rpc` attribute
    assert isinstance(result["netconf_sysrepo"].result.rpc, Manager)
