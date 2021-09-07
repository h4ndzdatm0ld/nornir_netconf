"""Nornir NETCONF Example Task: 'edit-config', 'netconf_lock'."""
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netconf.plugins.tasks import netconf_edit_config, netconf_lock


__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by 'west-region' assignment
west_region = nr.filter(region="west-region")


def example_global_lock(task):
    """Test global lock operation."""
    task.run(netconf_lock)


def main():
    """Execute Nornir Script."""
    print_result(west_region.run(task=example_netconf_get_capabilities))


if __name__ == "__main__":
    main()
