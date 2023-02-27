"""Test NETCONF get schemas unit test."""
from unittest.mock import MagicMock, patch

from ncclient.operations.rpc import RPCError, to_ele

from nornir_netconf.plugins.tasks import netconf_get_schemas

DEVICE_NAME = "nokia_rtr"


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


@patch("ncclient.manager.connect_ssh")
@patch("ncclient.manager.Manager")
def test_netconf_get_schema_schema_path(manager, ssh, nornir):
    """Test NETCONF Capabilities + Get Schemas success."""
    nr = nornir.filter(name=HOST)
    result = nr.run(netconf_get_schemas, schemas=["nokia-conf-aaa"], schema_path="tests/test_data/schema_path")
    assert not result[HOST].failed
    assert result[HOST].result.files[0] == "tests/test_data/schema_path/nokia-conf-aaa.txt"


@patch("ncclient.manager.connect_ssh")
@patch("ncclient.manager.Manager")
def test_netconf_get_schema(manager, ssh, nornir):
    """Test NETCONF get_schema, missing path"""
    manager.get_schema.return_value = str("SCHEMA")
    nr = nornir.filter(name=HOST)
    result = nr.run(netconf_get_schemas, schemas=["nokia-conf-aaa"], schema_path="/tmp")
    assert result[HOST].result.directory == "/tmp"


@patch("ncclient.manager.connect_ssh")
def test_netconf_get_schema_exception(ssh, nornir):
    """Test NETCONF Capabilities + Get Schemas failure, exception."""
    response = MagicMock()
    response.get_schema.side_effect = RPCError(to_ele(xml_resp))
    # Assign the side_effect to trigger on get_schema call and hit exception.
    ssh.side_effect = [response]

    nr = nornir.filter(name=HOST)
    result = nr.run(
        netconf_get_schemas, schemas=["nokia-conf-aaa", "some-other"], schema_path="tests/test_data/schema_path"
    )
    assert len(result[HOST].result.errors) == 2
