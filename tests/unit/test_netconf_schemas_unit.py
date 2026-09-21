"""Test NETCONF get schemas unit test."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from ncclient.operations.retrieve import GetSchemaReply
from ncclient.operations.rpc import RPCError, to_ele

from nornir_netconf.plugins.tasks import netconf_get_schemas
from nornir_netconf.plugins.tasks.retrieval.netconf_get_schemas import _schema_content, _schema_filename

DEVICE_NAME = "nokia_rtr"

YANG_SCHEMA = """module example {
  namespace "urn:example";
  prefix example;
}
"""

WRAPPED_SCHEMA = f"""<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring"><![CDATA[{YANG_SCHEMA}]]></data>
</rpc-reply>
"""


xml_resp = """
<rpc-reply message-id="urn:uuid:15ceca00-904e-11e4-94ad-5c514f91ab3f">
    <load-configuration-results>
        <rpc-error>
            <error-severity>error</error-severity>
            <error-info>
                <bad-element>system1</bad-element>
            </error-info>
            <error-message>syntax error</error-message>
        </rpc-error>
        <rpc-error>
            <error-severity>error</error-severity>
            <error-info>
                <bad-element>}</bad-element>
            </error-info>
            <error-message>error recovery ignores input until this point</error-message>
        </rpc-error>
    </load-configuration-results>
</rpc-reply>
"""


def test_schema_content_uses_parsed_data():
    """Use ncclient's parser with an XML declaration and CDATA wrapper."""
    assert _schema_content(GetSchemaReply(WRAPPED_SCHEMA)) == YANG_SCHEMA


def test_schema_content_uses_parsed_xml_element():
    """Use ncclient's parsed XML API when a device handler returns NCElement."""
    element = MagicMock(text=YANG_SCHEMA)
    schema_reply = MagicMock(data=None)
    schema_reply.xpath.return_value = [element]

    assert _schema_content(schema_reply) == YANG_SCHEMA
    schema_reply.xpath.assert_called_once_with("//*[local-name()='data']")


def test_schema_content_skips_empty_parsed_xml_elements():
    """Ignore empty data elements before accepting schema text."""
    schema_reply = MagicMock(data=None)
    schema_reply.xpath.return_value = [MagicMock(text=None), MagicMock(text=YANG_SCHEMA)]

    assert _schema_content(schema_reply) == YANG_SCHEMA


@pytest.mark.parametrize("schema", ["", ".", "..", "../example", "/tmp/example", r"..\example"])
def test_schema_filename_rejects_unsafe_identifiers(schema):
    """Schema identifiers cannot write outside the requested directory."""
    with pytest.raises(ValueError):
        _schema_filename(schema)


def test_schema_content_rejects_missing_data():
    """A malformed reply cannot be mistaken for a successfully downloaded schema."""
    schema_reply = MagicMock(data=None)
    schema_reply.xpath.return_value = []

    with pytest.raises(ValueError):
        _schema_content(schema_reply)


def test_schema_content_rejects_reply_without_parsed_data_api():
    """A reply without parsed schema data is rejected."""
    with pytest.raises(ValueError):
        _schema_content(object())


@patch("ncclient.manager.connect_ssh")
def test_netconf_get_schema_schema_path(ssh, nornir, tmp_path):
    """Test NETCONF Capabilities + Get Schemas success."""
    ssh.return_value.get_schema.return_value = GetSchemaReply(WRAPPED_SCHEMA)
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_get_schemas, schemas=["nokia-conf-aaa"], schema_path=str(tmp_path))
    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.files[0] == f"{tmp_path}/nokia-conf-aaa.yang"


@patch("ncclient.manager.connect_ssh")
def test_netconf_get_schema_writes_raw_yang(ssh, nornir, tmp_path):
    """Write schema data without the NETCONF RPC wrapper."""
    ssh.return_value.get_schema.return_value = GetSchemaReply(WRAPPED_SCHEMA)
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_get_schemas, schemas=["example"], schema_path=str(tmp_path))

    schema_file = Path(result[DEVICE_NAME].result.files[0])
    content = schema_file.read_text(encoding="utf-8")
    assert result[DEVICE_NAME].result.directory == str(tmp_path)
    assert content == YANG_SCHEMA
    assert "<rpc-reply" not in content


@patch("ncclient.manager.connect_ssh")
def test_netconf_get_schema_rejects_path_traversal(ssh, nornir, tmp_path):
    """A schema identifier cannot write outside schema_path."""
    ssh.return_value.get_schema.return_value = GetSchemaReply(WRAPPED_SCHEMA)
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_get_schemas, schemas=["../example"], schema_path=str(tmp_path))

    assert result[DEVICE_NAME].result.files == []
    assert result[DEVICE_NAME].result.errors == ["Invalid schema identifier: '../example'"]
    assert not (tmp_path.parent / "example.yang").exists()
    ssh.return_value.get_schema.assert_not_called()


@patch("ncclient.manager.connect_ssh")
def test_netconf_get_schema_rejects_missing_data(ssh, nornir, tmp_path):
    """A malformed reply is reported instead of being written as XML."""
    ssh.return_value.get_schema.return_value = MagicMock(data=None)
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_get_schemas, schemas=["example"], schema_path=str(tmp_path))

    assert result[DEVICE_NAME].result.files == []
    assert result[DEVICE_NAME].result.errors == ["NETCONF get-schema reply did not contain schema text."]
    assert not (tmp_path / "example.yang").exists()


@patch("ncclient.manager.connect_ssh")
def test_netconf_get_schema_exception(ssh, nornir):
    """Test NETCONF Capabilities + Get Schemas failure, exception."""
    response = MagicMock()
    response.get_schema.side_effect = RPCError(to_ele(xml_resp))
    # Assign the side_effect to trigger on get_schema call and hit exception.
    ssh.side_effect = [response]

    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(
        netconf_get_schemas, schemas=["nokia-conf-aaa", "some-other"], schema_path="tests/test_data/schema_path"
    )
    expected_results = 2
    assert len(result[DEVICE_NAME].result.errors) == expected_results
