"""Test Edit Config on Arista."""
from random import randint
from string import Template

from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import (
    netconf_commit,
    netconf_edit_config,
    netconf_get_config,
)
from tests.conftest import xml_dict

DEVICE_NAME = "ceos"

BFD_STATE = str(bool(randint(0, 1))).lower()
CONFIG_TEMPLATE = """
  <config>
    <bfd xmlns="http://openconfig.net/yang/bfd">
      <config xmlns="http://arista.com/yang/openconfig/bfd/augments">
        <enabled>${bfd_state}</enabled>
      </config>
    </bfd>
  </config>
  """
CONFIG = Template(CONFIG_TEMPLATE).substitute(bfd_state=BFD_STATE)


def test_edit_ceos_config(nornir):
    """Edit Config and then pull config to validate the change."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(task=netconf_edit_config, config=CONFIG, target="candidate")
    print_result(result)
    result = nr.run(task=netconf_commit)
    print_result(result)
    # Pull config and assert the default 'enabled' is set to dynamic variable `BFD_STATE`
    result = nr.run(
        netconf_get_config,
        source="running",
    )
    assert result[DEVICE_NAME].result.rpc
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    assert BFD_STATE == parsed["data"]["bfd"]["config"]["enabled"]
