"""Test Helper functions."""
import os
import pathlib
from unittest.mock import patch

from nornir_netconf.plugins.helpers import check_capability, create_folder, write_output

TEST_FOLDER = "tests/test_data/test_folder_success"


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
    path = pathlib.Path(folder)
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


def test_check_capability_false():
    """Test check_capability failure.

    Remove candidate from list.
    """
    capabilities.pop(2)
    assert not check_capability(capabilities, "candidate")
