# type: ignore
"""Nornir NETCONF Example Task: 'capabilities'."""
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netconf.plugins.tasks import netconf_capabilities


__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by 'west-region' assignment
west_region = nr.filter(region="west-region")


def example_netconf_get_capabilities(task):
    """Test get capabilities."""
    task.run(netconf_capabilities)


def main():
    """Execute Nornir Script."""
    print_result(west_region.run(task=example_netconf_get_capabilities))


if __name__ == "__main__":
    main()
