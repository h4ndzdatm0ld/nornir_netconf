"""Test NETCONF get schemas unit test."""
# from nornir_utils.plugins.functions import print_result
from unittest.mock import patch

# from nornir_utils.plugins.functions import print_result

# from ncclient.operations.rpc import RPCError, to_ele
from nornir_netconf.plugins.tasks import netconf_get_schemas

xml6 = """<rpc-error xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
			<error-type>application</error-type>
			<error-tag>invalid-value</error-tag>
			<error-severity>error</error-severity>
			<error-path>path/to/node</error-path>
			<error-info>
				<bad-element>system1</bad-element>
			</error-info>
			<error-app-tag>app-tag1</error-app-tag>
			<error-message>syntax error</error-message>
	  </rpc-error>
"""


@patch("ncclient.manager.Manager")
def test_netconf_get_schema(manager, nornir):
    """Test NETCONF get_schema, missing path"""
    manager.get_schema.return_value = str("SCHEMA")
    nr = nornir.filter(name="netconf1")
    result = nr.run(netconf_get_schemas, schemas=["nokia-conf-aaa"])
    assert result["netconf1"].failed
    assert result["netconf1"].result["errors"][0] == "Missing 'schema_path' arg to save schema files."


@patch("ncclient.manager.Manager")
def test_netconf_get_schema_schema_path(manager, nornir_unittest):
    """Test NETCONF Capabilities + Get Schemas success."""
    nr = nornir_unittest.filter(name="netconf1")
    result = nr.run(netconf_get_schemas, schemas=["nokia-conf-aaa"], schema_path="tests/test_data/schema_path")
    assert not result["netconf1"].failed
    assert result["netconf1"].result["log"][0] == "tests/test_data/schema_path/nokia-conf-aaa.txt created."

