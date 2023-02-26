from nornir_netconf.plugins.tasks import netconf_get_config
from tests.conftest import xml_dict

HOST = "ceos"


def test_netconf_get_config_running(nornir):
    """Test get running config as default."""
    nr = nornir.filter(name=HOST)

    result = nr.run(netconf_get_config, source="running")
    assert result[HOST].result.rpc.ok
    parsed = xml_dict(result[HOST].result.rpc.data_xml)
    assert parsed["data"]["system"]["config"]["hostname"] == "ceos"


def test_netconf_get_config_subtree(nornir):
    """Test filter subtree of get_config."""
    nr = nornir.filter(name=HOST)
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
    assert result[HOST].result.rpc.ok
    parsed = xml_dict(result[HOST].result.rpc.data_xml)
    assert parsed["data"]["interfaces"]["interface"]["name"] == "Management1"
