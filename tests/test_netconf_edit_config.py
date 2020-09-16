from nornir_netconf.plugins.tasks import netconf_edit_config, netconf_get_config


CONFIG = """
<nc:config
    xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <turing-machine
        xmlns="http://example.net/turing-machine">
        <transition-function>
            <delta nc:operation="{operation}">
                <label>this-is-nornir</label>
                <input>
                    <symbol>4</symbol>
                    <state>1</state>
                </input>
            </delta>
        </transition-function>
    </turing-machine>
</nc:config>
"""


def test_netconf_edit_config(nornir):
    nr = nornir.filter(name="netconf1.no_group")
    assert nr.inventory.hosts

    result = nr.run(netconf_get_config)

    for _, v in result.items():
        assert "nornir" not in v.result

    result = nr.run(
        netconf_edit_config,
        config=CONFIG.format(operation="merge"),
        target="candidate",
    )

    assert not result.failed
    assert "<nc:ok/>" in result["netconf1.no_group"].result

    result = nr.run(netconf_get_config, source="candidate")

    for _, v in result.items():
        assert "nornir" in v.result

    status = nr.run(
        netconf_edit_config,
        config=CONFIG.format(operation="delete"),
        target="candidate",
    )
    assert not status.failed

    result = nr.run(netconf_get_config, source="candidate")

    for _, v in result.items():
        assert "nornir" not in v.result
