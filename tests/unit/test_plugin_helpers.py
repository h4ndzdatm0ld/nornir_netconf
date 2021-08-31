"""Test Helper functions."""
from unittest import mock

import ncclient

from nornir_netconf.plugins.helpers import get_result


@mock.patch.object(ncclient.xml_, "NCElement")
def test_get_result_rpc_ok(nce_element):
    """Test get result failed."""
    nce_element.ok = True

    result = get_result(nce_element)
    assert not result["failed"]
    assert result["result"]["ok"]


@mock.patch.object(ncclient.xml_, "NCElement")
def test_get_result(nce_element):
    """Test get result failed."""
    nce_element.ok = False
    nce_element.data_xml = False
    result = get_result(nce_element)
    assert result["failed"]
    assert not result["result"]
