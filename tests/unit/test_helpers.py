"""Test Helper functions."""
from typing import OrderedDict
from unittest import mock

import ncclient

from nornir_netconf.plugins.helpers import get_result


def test_get_result_attr_error():
    """Test get result - attr error."""

    result = get_result({"name": "prometheus"})
    assert result["failed"]


@mock.patch.object(ncclient.xml_, "NCElement")
def test_get_result_rpc_ok(nce_element):
    """Test get result failed."""
    nce_element.ok = True

    result = get_result(nce_element)
    assert not result["failed"]
    assert result["result"]["ok"]


@mock.patch.object(ncclient.xml_, "NCElement")
def test_get_result_failed(nce_element):
    """Test get result failed."""
    nce_element.ok = False
    nce_element.data_xml = False
    result = get_result(nce_element)
    assert result["failed"]
    assert not result["result"]["ok"]
    assert not result["result"]["errors"]


@mock.patch.object(ncclient.xml_, "NCElement")
def test_get_result_rpc_no_ok_but_data_xml(nce_element):
    """Test get result failed."""
    nce_element.ok = False
    nce_element.data_xml = "<configure></configure>"

    result = get_result(nce_element)
    assert not result["failed"]
    assert not result["result"]["error"]
    assert not result["result"]["errors"]
    assert isinstance(result["result"]["xml_dict"], OrderedDict)
