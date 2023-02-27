"""Integration Testing Deploying L3VPN via Netconf."""
from nornir_netconf.plugins.tasks import netconf_commit, netconf_edit_config
from tests.conftest import skip_integration_tests

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

    # Edit Config
    result = nr.run(task=netconf_edit_config, target="candidate", config=DEPLOY_SERVICE)

    # Commit Config
    result = nr.run(netconf_commit)
    assert result[DEVICE_NAME].result.rpc.ok
