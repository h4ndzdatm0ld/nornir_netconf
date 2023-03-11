"""Test NETCONF schemas."""
from nornir_netconf.plugins.tasks import netconf_get_schemas
from tests.conftest import skip_integration_tests

DEVICE_NAME = "nokia_rtr"


@skip_integration_tests
def test_netconf_capabilities_get_schema(nornir, schema_path):
    """Test NETCONF Capabilities + Get Schemas success."""
    nr = nornir.filter(name="nokia_rtr")
    result = nr.run(netconf_get_schemas, schemas=["nokia-bof-state"], schema_path=schema_path)
    assert result[DEVICE_NAME].result["log"][0] == "tests/test_data/schema_path/nokia-bof-state.txt created."


@skip_integration_tests
def test_netconf_capabilities_get_schema_errors(nornir, schema_path):
    """Test NETCONF Capabilities + Get Schemas unrecognized schema name."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_get_schemas, schemas=["nokia-conf-aaa", "ok"], schema_path=schema_path)
    assert not result[DEVICE_NAME].result.files
    assert result[DEVICE_NAME].result.errors[0] == "MINOR: MGMT_CORE #2301: Invalid element value"
