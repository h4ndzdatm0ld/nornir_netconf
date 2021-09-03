"""Test Helper functions."""
import os
import pathlib
from unittest import mock
from unittest.mock import patch

import ncclient
from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.helpers import create_folder, get_result, write_output, xml_to_dict

TEST_FOLDER = "tests/test_data/test_folder_success"


def test_xml_to_dict_exception():
    """Test xml_to_dict."""
    result = xml_to_dict({"test": "data"})
    assert result == {"error": "Unable to parse XML to Dict. 'dict' object has no attribute 'data_xml'."}


def test_get_result_attr_error():
    """Test get result - attr error."""

    result = get_result({"name": "prometheus"})
    assert result["failed"]


# Test Create Folder


def test_create_folder(test_folder):
    """Test create_folder success."""
    create_folder(test_folder)
    assert os.path.exists(test_folder)


def test_create_folder_exists(test_folder):
    """Test create_folder already exists success."""
    create_folder(test_folder)
    assert os.path.exists(test_folder)


@patch("os.makedirs", side_effect=OSError)
def test_create_folder_exception(os_mock, test_folder):
    """Test create_folder failure."""
    folder = f"{test_folder}/test"
    create_folder(folder)

    # using pathlib as we patched OS
    path = pathlib.Path("folder")
    assert not path.exists()


# Test Write Output


def test_write_output_success_new_path(test_folder):
    """Test write output success."""
    test_folder = f"{test_folder}/folder"
    write_output("test-text", test_folder, "file-name")
    assert os.path.exists(f"{test_folder}/file-name.txt")


def test_write_output_success_already_exists(test_folder):
    """Test write output success."""
    write_output("test-text", test_folder, "file-name")
    assert os.path.exists(f"{test_folder}/file-name.txt")


@mock.patch.object(ncclient.xml_, "NCElement")
def test_get_result_rpc_ok(nce_element):
    """Test get result failed."""
    nce_element.ok = True

    result = get_result(nce_element, xmldict=True)
    assert not result["failed"]
    assert result["result"]["ok"]


def test_get_result_failed():
    """Test get result failed."""
    data = {"ok": False}
    result = get_result(data, xmldict=True)
    assert result["failed"]
    assert not result["result"]["ok"]
    assert result["result"]["errors"] == "Unable to find 'ok' or data_xml in response object."


@mock.patch.object(ncclient.xml_, "NCElement")
def test_get_result_rpc_no_ok_but_data_xml(nce_element):
    """Test get result failed."""
    nce_element.ok = False
    nce_element.data_xml = "<configure></configure>"
    result = get_result(nce_element, xmldict=True)
    assert not result["failed"]
    assert not result["result"]["error"]
    assert not result["result"]["errors"]
    assert "configure" in result["result"]["xml_dict"].keys()
    print_result(result)


@mock.patch.object(ncclient.xml_, "NCElement")
def test_get_result_rpc_no_xml_dict(nce_element):
    """Test get result failed."""
    nce_element.ok = False
    nce_element.data_xml = True

    result = get_result(nce_element)
    assert not result["failed"]
    assert not result["result"]["error"]
    assert not result["result"]["errors"]


# Test Get Results


class FakeRpcObject:
    """Test Class."""

    def __init__(self):
        self.ok = False
        self.error = ""
        self.errors = ""
        self.data_xml = False

    def set_ok(self, set: bool):
        """Set ok."""
        if set:
            self.ok = True

    def set_data_xml(self, set: bool):
        """Set data_xml."""
        if set:
            self.data_xml = True


class FakeRpcObjectNoData:
    """Test Class."""

    def __init__(self):
        self.ok = False
        self.error = ""
        self.errors = ""


class FakeRpcObjectSlim:
    """Test Class."""

    def __init__(self):
        self.error = ""
        self.errors = ""
        self.data_xml = ""


def test_get_result_rpc_slim():
    """Test get result failed, not a Dict, no any 'ok'."""

    test_object = FakeRpcObjectSlim()
    result = get_result(test_object)
    assert result["failed"]


def test_get_result_rpc_ok_no_data_xml():
    """Test get result ok, no data_xml."""

    test_object = FakeRpcObject()
    test_object.set_ok(set=True)

    result = get_result(test_object)
    assert not result["failed"]
    assert result["result"]["ok"]


def test_get_result_rpc_ok_true():
    """Test get result ok."""

    test_object = FakeRpcObject()
    test_object.set_ok(set=False)

    result = get_result(test_object)
    assert not result["failed"]
    assert result["result"]["ok"]
