"""Integration test configuration edits against IOSXE device."""

from random import randint
from string import Template

from nornir_netconf.plugins.tasks import netconf_edit_config, netconf_get_config
from tests.conftest import skip_integration_tests, xml_dict

# from nornir_utils.plugins.functions import print_result


DEVICE_NAME = "iosxe_rtr"

RANDOM_DESCRIPTION = f"NORNIR-NETCONF-DESCRIPTION-{randint(0, 100)}"
CONFIG_TEMPLATE = """
  <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="http://openconfig.net/yang/interfaces">
      <interface>
        <name>GigabitEthernet1</name>
        <config>
          <name>GigabitEthernet1</name>
          <description>${random_description}</description>
        </config>
      </interface>
    </interfaces>
  </config>
  """
CONFIG = Template(CONFIG_TEMPLATE).substitute(random_description=RANDOM_DESCRIPTION)


@skip_integration_tests
def test_netconf_edit_config(nornir):
    """Test Edit Config."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(task=netconf_edit_config, config=CONFIG, target="running")
    assert result[DEVICE_NAME].result.rpc.ok

    # Validate config change is in running config datastore
    result = nr.run(
        netconf_get_config,
        source="running",
    )
    assert result[DEVICE_NAME].result.rpc
    assert result[DEVICE_NAME].result.rpc.data_xml
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    assert RANDOM_DESCRIPTION == parsed["data"]["interfaces"][0]["interface"]["description"]
