"""Integration test against IOSXR device."""
from random import randint
from string import Template

from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import (
    netconf_commit,
    netconf_edit_config,
    netconf_get_config,
)
from tests.conftest import skip_integration_tests, xml_dict

DEVICE_NAME = "iosxr_rtr"
RANDOM_TIMER = randint(10, 100)
CONFIG_TEMPLATE = """
<config xmlns:xc="urn:ietf:params:xml:n:netconf:base:1.0">
    <cdp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-cdp-cfg">
        <timer>${timer}</timer>
        <enable>true</enable>
        <log-adjacency></log-adjacency>
        <hold-time>200</hold-time>
        <advertise-v1-only></advertise-v1-only>
    </cdp>
</config>
"""
CONFIG = Template(CONFIG_TEMPLATE).substitute(timer=RANDOM_TIMER)


@skip_integration_tests
def test_iosxr_netconf_edit_config(nornir):
    """Test NETCONF edit-config from candidate datastore and commit."""
    nr = nornir.filter(name=DEVICE_NAME)
    result = nr.run(netconf_edit_config, config=CONFIG, target="candidate")
    assert result[DEVICE_NAME].result.rpc.ok
    print_result(result)

    # Commit Config
    result = nr.run(netconf_commit)
    assert result[DEVICE_NAME].result.rpc.ok
    print_result(result)

    result = nr.run(
        netconf_get_config,
        source="running",
    )
    print_result(result)

    assert result[DEVICE_NAME].result.rpc
    assert result[DEVICE_NAME].result.rpc.data_xml
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    assert str(RANDOM_TIMER) == parsed["data"]["cdp"]["timer"]
