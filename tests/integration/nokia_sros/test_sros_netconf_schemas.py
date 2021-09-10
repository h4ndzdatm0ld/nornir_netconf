"""Test NETCONF schemas."""
from nornir_netconf.plugins.tasks import netconf_get_schemas
from tests.conftest import skip_integration_tests


@skip_integration_tests
def test_netconf_capabilities_get_schema(nornir, schema_path):
    """Test NETCONF Capabilities + Get Schemas success."""
    nr = nornir.filter(name="nokia_rtr")
    result = nr.run(netconf_get_schemas, schemas=["nokia-conf-aaa"], schema_path=schema_path)
    assert result["nokia_rtr"].result["log"][0] == "tests/test_data/schema_path/nokia-conf-aaa.txt created."
    assert not result["nokia_rtr"].result["errors"]


@skip_integration_tests
def test_netconf_capabilities_get_schema_errors(nornir, schema_path):
    """Test NETCONF Capabilities + Get Schemas unrecognized schema name."""
    nr = nornir.filter(name="nokia_rtr")
    result = nr.run(netconf_get_schemas, schemas=["nokia-conf-aaa", "ok"], schema_path=schema_path)
    assert result["nokia_rtr"].result["log"][0] == "tests/test_data/schema_path/nokia-conf-aaa.txt created."
    assert result["nokia_rtr"].result["errors"][0] == "MINOR: MGMT_CORE #2301: Invalid element value"
