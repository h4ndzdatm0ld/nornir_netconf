from nornir_netconf.plugins.tasks import netconf_get_config
from tests.conftest import xml_dict

DEVICE_NAME = "ceos"


def test_netconf_get_config_running(nornir):
    """Test get running config as default."""
    nr = nornir.filter(name=DEVICE_NAME)

    result = nr.run(netconf_get_config, source="running")
    assert result[DEVICE_NAME].result.rpc.ok
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    assert parsed["data"]["system"]["config"]["hostname"] == "ceos"


def test_netconf_get_config_subtree(nornir):
    """Test filter subtree of get_config."""
    nr = nornir.filter(name=DEVICE_NAME)
    eth3 = """
    <interfaces>
        <interface>
            <name>Management1</name>
        </interface>
    </interfaces>
    """
    result = nr.run(
        netconf_get_config,
        source="running",
        path=eth3,
        filter_type="subtree",
    )
    assert result[DEVICE_NAME].result.rpc.ok
    parsed = xml_dict(result[DEVICE_NAME].result.rpc.data_xml)
    assert parsed["data"]["interfaces"]["interface"]["name"] == "Management1"
