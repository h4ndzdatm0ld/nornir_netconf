"""Helpers Unit Tests."""

from nornir_netconf.plugins.helpers import check_file


def test_check_file():
    """Test false check_file."""
    assert not check_file("somebadpath.json")
