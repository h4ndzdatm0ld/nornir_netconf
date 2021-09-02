# """Test NETCONF get schemas unit test."""
# from nornir_utils.plugins.functions import print_result

# from nornir_netconf.plugins.tasks import netconf_get_schemas


# def test_netconf_capabilities_get_schema(nornir):
#     """Test NETCONF Capabilities + Get Schemas success."""
#     nr = nornir.filter(name="nokia_rtr")
#     result = nr.run(netconf_get_schemas, schemas=["nokia-conf-aaa"], schema_path="tests/test_data/schema_path")
#     print_result(result)
#     # assert not result["netconf1"].failed
