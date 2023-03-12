"""Test Get Schemas from all vendors."""
from typing import Dict

from nornir.core.filter import F

from nornir_netconf.plugins.tasks import netconf_get, netconf_get_schemas
from tests.conftest import skip_integration_tests, xml_dict

# from nornir_utils.plugins.functions import print_result


@skip_integration_tests
def test_netconf_capabilities_get_schema(nornir, schema_path):
    """Test NETCONF Capabilities + Get Schemas success."""
    nr = nornir.filter(F(groups__contains="integration"))
    hosts = list(nr.inventory.hosts.keys())
    schema_map: Dict[str, str] = {}

    filter = """
    <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
        <schemas>
        </schemas>
    </netconf-state>
    """
    result = nr.run(netconf_get, path=filter, filter_type="subtree")
    for host in hosts:
        assert not result[host][0].failed
        parsed = xml_dict(result[host][0].result.rpc.data_xml)
        if "rpc-reply" in list(parsed.keys()):
            first_schema = parsed["rpc-reply"]["data"]["netconf-state"]["schemas"]["schema"][0]

        else:
            first_schema = parsed["data"]["netconf-state"]["schemas"]["schema"][0]
        schema_map.setdefault(host, first_schema["identifier"])
        # example = {
        #     "identifier": "iana-if-type",
        #     "version": "2014-05-08",
        #     "format": "yang",
        #     "namespace": "urn:ietf:params:xml:ns:yang:iana-if-type",
        #     "location": "NETCONF",
        # }
    for host in hosts:
        nr = nornir.filter(name=host)
        schema = nr.run(netconf_get_schemas, schemas=[schema_map[host]], schema_path=schema_path)
        assert schema[host].result.files
        assert not schema[host].result.errors
        assert schema[host].result.directory
