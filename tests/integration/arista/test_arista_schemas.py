"""Test NETCONF schema retrieval on Arista."""

from pathlib import Path

from nornir_netconf.plugins.tasks import netconf_get, netconf_get_schemas
from tests.conftest import skip_integration_tests, xml_dict

DEVICE_NAME = "ceos"
pytestmark = skip_integration_tests

SCHEMA_FILTER = """
<netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
  <schemas/>
</netconf-state>
"""


def test_netconf_get_schema_writes_raw_yang(nornir, schema_path):
    """Downloaded schemas contain YANG text without the NETCONF wrapper."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_get, path=SCHEMA_FILTER, filter_type="subtree")
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    reply = parsed.get("rpc-reply", parsed)
    first_schema = reply["data"]["netconf-state"]["schemas"]["schema"][0]

    result = nr.run(
        netconf_get_schemas,
        schemas=[first_schema["identifier"]],
        schema_path=schema_path,
    )

    schema_file = Path(result[DEVICE_NAME].result.files[0])
    content = schema_file.read_text(encoding="utf-8")
    assert not result[DEVICE_NAME].result.errors
    assert not content.lstrip().startswith("<?xml")
    assert "<rpc-reply" not in content
    assert content.lstrip().startswith(("module ", "submodule "))
