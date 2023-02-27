# from nornir_netconf.plugins.tasks import netconf_edit_config, netconf_get_config
# from nornir_utils.plugins.functions import print_result

# CONFIG = """
# <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
#     <netconf-server xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-server">
#         <listen>
#             <endpoint>
#                 <name>default-ssh-updated</name>
#             </endpoint>
#         </listen>
#     </netconf-server>
# </config>
# """


# def test_netconf_edit_config(nornir):
#     nr = nornir.filter(name="netconf_sysrepo")
#     assert nr.inventory.hosts

#     result = nr.run(netconf_get_config)

#     for _, v in result.items():
#         assert "nornir" not in v.result

#     result = nr.run(netconf_edit_config, config=CONFIG, target="running")
#     print_result(result)
#     assert not result.failed
#     assert "<nc:ok/>" in result["netconf_sysrepo"].result

# result = nr.run(netconf_get_config, source="candidate")

# for _, v in result.items():
#     assert "nornir" in v.result

# status = nr.run(netconf_edit_config, config=CONFIG.format(operation="delete"), target="candidate",)
# assert not status.failed

# result = nr.run(netconf_get_config, source="candidate")

# for _, v in result.items():
#     assert "nornir" not in v.result
