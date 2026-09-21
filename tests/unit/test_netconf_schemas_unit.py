"""Test NETCONF get schemas unit test."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from ncclient.operations.rpc import RPCError, to_ele

from nornir_netconf.plugins.tasks import netconf_get_schemas
from nornir_netconf.plugins.tasks.retrieval.netconf_get_schemas import _schema_content

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


class SchemaReply:
    """Minimal ncclient GetSchemaReply test double."""

    data = YANG_SCHEMA

    def __str__(self) -> str:
        return WRAPPED_SCHEMA


def test_schema_content_uses_parsed_data():
    """Use ncclient's parsed data even when the XML reply has a declaration."""
    assert _schema_content(SchemaReply()) == YANG_SCHEMA


def test_schema_content_supports_string_test_doubles():
    """Keep compatibility with callers returning a plain string."""
    assert _schema_content(YANG_SCHEMA) == YANG_SCHEMA


@patch("ncclient.manager.connect_ssh")
@patch("ncclient.manager.Manager")
def test_netconf_get_schema_schema_path(manager, ssh, nornir):
    """Test NETCONF Capabilities + Get Schemas success."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_get_schemas, schemas=["nokia-conf-aaa"], schema_path="tests/test_data/schema_path")
    assert not result[DEVICE_NAME].failed
    assert result[DEVICE_NAME].result.files[0] == "tests/test_data/schema_path/nokia-conf-aaa.yang"


@patch("ncclient.manager.connect_ssh")
def test_netconf_get_schema_writes_raw_yang(ssh, nornir, tmp_path):
    """Write schema data without the NETCONF RPC wrapper."""
    ssh.return_value.get_schema.return_value = SchemaReply()
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_get_schemas, schemas=["example"], schema_path=str(tmp_path))

    schema_file = Path(result[DEVICE_NAME].result.files[0])
    assert result[DEVICE_NAME].result.directory == str(tmp_path)
    assert schema_file.read_text(encoding="utf-8") == YANG_SCHEMA
    assert "<rpc-reply" not in schema_file.read_text(encoding="utf-8")


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
