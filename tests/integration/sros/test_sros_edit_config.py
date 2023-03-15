"""Integration Testing Deploying L3VPN via Netconf to candidate datastore and committing."""
from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import (
    netconf_commit,
    netconf_edit_config,
    netconf_get_config,
    netconf_validate,
)
from tests.conftest import CONFIGS_DIR, skip_integration_tests, xml_dict

DEVICE_NAME = "nokia_rtr"

DEPLOY_SERVICE = """
<config>
  <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
    <service>
      <customer>
        <customer-name>AVIFI-CO</customer-name>
        <customer-id>200</customer-id>
      </customer>
      <vprn>
        <service-name>AVIFI</service-name>
        <service-id>100</service-id>
        <admin-state>enable</admin-state>
        <customer>AVIFI-CO</customer>
        <autonomous-system>64500</autonomous-system>
        <vprn-type>regular</vprn-type>
        <bgp-ipvpn>
          <mpls>
            <admin-state>enable</admin-state>
            <route-distinguisher>64500:100</route-distinguisher>
            <vrf-target>
              <community>target:64500:100</community>
            </vrf-target>
            <auto-bind-tunnel>
              <resolution>any</resolution>
            </auto-bind-tunnel>
          </mpls>
        </bgp-ipvpn>
        <interface>
          <interface-name>TEST-LOOPBACK</interface-name>
          <loopback>true</loopback>
          <ipv4>
              <primary>
                  <address>3.3.3.3</address>
                  <prefix-length>32</prefix-length>
              </primary>
          </ipv4>
        </interface>
      </vprn>
    </service>
  </configure>
</config>
"""


@skip_integration_tests
def test_sros_netconf_edit_config_service(nornir):
    """Test NETCONF edit-config."""
    nr = nornir.filter(name=DEVICE_NAME)
    # Edit Candidate Config
    result = nr.run(task=netconf_edit_config, target="candidate", config=DEPLOY_SERVICE)
    assert not result[DEVICE_NAME].failed
    validate = nr.run(task=netconf_validate)
    print_result(validate)
    # Commit Config into `Running` datastore
    result = nr.run(netconf_commit)
    assert not result[DEVICE_NAME].failed
    # Grab Full Config from datastore
    result = nr.run(
        netconf_get_config,
        source="running",
    )
    with open(f"{CONFIGS_DIR}/{DEVICE_NAME}-full-config-post.xml", "w+") as file:
        file.write(result[DEVICE_NAME].result.rpc.data_xml)
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    assert "AVIFI-CO" == parsed["rpc-reply"]["data"]["configure"]["service"]["customer"]["customer-name"]
