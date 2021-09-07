"""Nornir NETCONF Example Task: 'get-config'."""
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netconf.plugins.tasks import netconf_get_config


__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by 'west-region' assignment
west_region = nr.filter(region="west-region")


def example_netconf_get_config(task):
    """Test get config."""
    task.run(
        netconf_get_config,
        source="running",
        path="""
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <router>
                <router-name>Base</router-name>
            </router>
        </configure>
        """,
        filter_type="subtree",
    )


def main():
    """Execute Nornir Script."""
    print_result(west_region.run(task=example_netconf_get_config))


if __name__ == "__main__":
    main()
