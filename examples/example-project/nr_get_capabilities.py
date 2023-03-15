# type: ignore
"""Nornir NETCONF Example Task: 'capabilities'."""
from nornir import InitNornir
from nornir.core.task import Task
from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import netconf_capabilities

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by 'west-region' assignment
west_region = nr.filter(region="west-region")


def example_netconf_get_capabilities(task: Task) -> str:
    """Test get capabilities."""
    capabilities = task.run(netconf_capabilities)
    # This may be a lot, so for example we'll just print the first one
    return [cap for cap in capabilities.result.rpc][0]


def main():
    """Execute Nornir Script."""
    print_result(west_region.run(task=example_netconf_get_capabilities))


if __name__ == "__main__":
    main()
