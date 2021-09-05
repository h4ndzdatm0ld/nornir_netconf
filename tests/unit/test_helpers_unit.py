"""Test Helper functions."""
import os
import pathlib
from unittest import mock
from unittest.mock import patch

import ncclient

from nornir_netconf.plugins.helpers import (
    create_folder,
    get_result,
    write_output,
    xml_to_dict,
    check_capability,
)
from tests.conftest import FakeRpcObject

TEST_FOLDER = "tests/test_data/test_folder_success"


def test_xml_to_dict_exception():
    """Test xml_to_dict."""
    result = xml_to_dict({"test": "data"})
    assert result == {"error": "Unable to parse XML to Dict. 'dict' object has no attribute 'data_xml'."}


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


# Test Get Results


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


class FakeRpcObjectAny:
    """Test Class."""

    def __init__(self):
        self.error = ""
        self.errors = ""


class FakeRpcObjectXml:
    """Test Class."""

    def __init__(self):
        self.error = ""
        self.errors = ""
        self.data_xml = "<configure><router></router></configure>"


def test_get_result_rpc_slim():
    """Test get result failed, not a Dict, no any 'ok'.

    Get results will re-create the 'ok' attr.
    """

    test_object = FakeRpcObjectSlim()
    result = get_result(test_object)
    assert not result["failed"]


def test_get_result_attr_error():
    """Test get result - attr error."""

    result = get_result({"name": "prometheus"})
    assert result["failed"]


def test_get_result_rpc_ok_no_data_xml():
    """Test get result ok, no data_xml."""

    test_object = FakeRpcObject()
    test_object.set_ok(set=True)

    result = get_result(test_object)
    assert not result["failed"]
    assert result["result"]["ok"]


def test_get_result_ok_false():
    """Test get result ok."""

    test_object = FakeRpcObject()
    test_object.set_ok(set=False)

    result = get_result(test_object)
    assert result["failed"]
    assert not result["result"]["ok"]


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
    assert result["failed"]
    assert "configure" in result["result"]["xml_dict"].keys()


def test_get_result_skip_any():
    """Test get result failed."""
    test_object = FakeRpcObjectAny()

    result = get_result(test_object)
    assert result["failed"]


def test_get_result_skip_ok_xml_dict():
    """Test get result hit any, skip ok, xmldict."""
    test_object = FakeRpcObjectXml()

    result = get_result(test_object, xmldict=True)
    assert not result["failed"]


capabilities = [
    "urn:ietf:params:netconf:base:1.0",
    "urn:ietf:params:netconf:base:1.1",
    "urn:ietf:params:netconf:capability:candidate:1.0",
    "urn:ietf:params:netconf:capability:confirmed-commit:1.1",
    "urn:ietf:params:netconf:capability:rollback-on-error:1.0",
    "urn:ietf:params:netconf:capability:notification:1.0",
    "urn:ietf:params:netconf:capability:interleave:1.0",
    "urn:ietf:params:netconf:capability:validate:1.0",
    "urn:ietf:params:netconf:capability:validate:1.1",
    "urn:ietf:params:netconf:capability:startup:1.0",
    "urn:ietf:params:netconf:capability:url:1.0?scheme=ftp,tftp,file",
    "urn:ietf:params:netconf:capability:with-defaults:1.0?basic-mode=explicit&also-supported=report-all",
    "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring",
    "urn:ietf:params:netconf:capability:yang-library:1.0?revision=2016-06-21&module-set-id=20.5.R2",
    "urn:nokia.com:sros:ns:yang:sr:major-release-20",
    "urn:ietf:params:xml:ns:yang:iana-if-type?module=iana-if-type&revision=2014-05-08",
    "urn:ietf:params:xml:ns:yang:ietf-inet-types?module=ietf-inet-types&revision=2013-07-15",
]


def test_check_capability_true():
    """Test check_capability success."""
    assert check_capability(capabilities, "candidate")


def test_check_capability_true():
    """Test check_capability failure.

    Remove candidate from list.
    """
    capabilities.pop(2)
    assert not check_capability(capabilities, "candidate")
