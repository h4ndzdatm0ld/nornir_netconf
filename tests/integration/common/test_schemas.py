"""Test Get Schemas from all vendors."""
from typing import Dict

from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import netconf_get, netconf_get_schemas
from tests.conftest import CONFIGS_DIR, skip_integration_tests, xml_dict

CEOS_EXPECTED_SCHEMA = "nokia-bof-state"
SROS_EXPECTED_SCHEMA = "nokia-bof-state"
IOSXE_EXPECTED_SCHEMA = "nokia-bof-state"
IOSXR_EXPECTED_SCHEMA = "nokia-bof-state"

SCHEMAS: Dict = {
    "ceos": CEOS_EXPECTED_SCHEMA,
    "iosxe_rtr": IOSXE_EXPECTED_SCHEMA,
    "nokia_rtr": SROS_EXPECTED_SCHEMA,
    "iosxr_rtr": IOSXR_EXPECTED_SCHEMA,
}


# @skip_integration_tests
def test_netconf_capabilities_get_schema(nornir, schema_path):
    """Test NETCONF Capabilities + Get Schemas success."""
    nr = nornir.filter(F(groups__contains="integration"))
    hosts = list(nr.inventory.hosts.keys())
    schema_map: Dict = {}

    filter = """
    <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
        <schemas>
        </schemas>
    </netconf-state>
    """
    result = nr.run(netconf_get, path=filter, filter_type="subtree")
    for host in hosts:
        parsed = xml_dict(result[host][0].result.rpc.data_xml)
        if "rpc-reply" in list(parsed.keys()):
            first_schema = parsed["rpc-reply"]["data"]["netconf-state"]["schemas"]["schema"][6]

        else:
            first_schema = parsed["data"]["netconf-state"]["schemas"]["schema"][6]
        schema_map.setdefault(host, first_schema["identifier"])

        # example = {
        #     "identifier": "iana-if-type",
        #     "version": "2014-05-08",
        #     "format": "yang",
        #     "namespace": "urn:ietf:params:xml:ns:yang:iana-if-type",
        #     "location": "NETCONF",
        # }
    print(schema_map)
    for host in hosts:
        nr = nornir.filter(name=host)
        schema = nr.run(netconf_get_schemas, schemas=[schema_map[host]], schema_path=schema_path)
        if schema[host].failed:
            breakpoint()
        # assert schema[host].result.files
        # assert not schema[host].result.errors
        # assert schema[host].result.directory


# @skip_integration_tests
# def test_netconf_capabilities_get_schema_errors(nornir, schema_path):
#     """Test NETCONF Capabilities + Get Schemas unrecognized schema name."""
#     nr = nornir.filter(name=DEVICE_NAME)
#     result = nr.run(netconf_get_schemas, schemas=["nokia-conf-aaa", "ok"], schema_path=schema_path)
#     assert not result[DEVICE_NAME].result.files
#     assert result[DEVICE_NAME].result.errors[0] == "MINOR: MGMT_CORE #2301: Invalid element value"
