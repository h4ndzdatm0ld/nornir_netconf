# type: ignore
"""Nornir NETCONF Example Task: 'edit-config', 'netconf_lock', `netconf_commit`, and `netconf_validate"""
from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import (
    netconf_commit,
    netconf_edit_config,
    netconf_lock,
    netconf_validate,
)

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by 'west-region' assignment
west_region = nr.filter(region="west-region")


def example_global_lock(task: Task) -> Result:
    """Test global lock operation of 'candidate' datastore."""
    lock = task.run(netconf_lock, datastore="candidate", operation="lock")
    # Retrieve the Manager(agent) from lock operation and store for further
    # operations.
    task.host["manager"] = lock.result.manager


def example_edit_config(task: Task) -> Result:
    """Test edit-config with global lock using manager agent."""
    config_payload = """
    <config>
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <router>
                <router-name>Base</router-name>
                <interface>
                    <interface-name>L3-OAM-eNodeB069420-X1</interface-name>
                    <admin-state>disable</admin-state>
                    <ingress-stats>false</ingress-stats>
                </interface>
            </router>
        </configure>
    </config>
    """

    task.run(netconf_edit_config, config=config_payload, target="candidate", manager=task.host["manager"])
    # Validate the candidate configuration
    task.run(netconf_validate)
    # Commit configuration
    task.run(netconf_commit, manager=task.host["manager"])


def example_unlock(task: Task) -> Result:
    """Unlock candidate datastore."""
    task.run(netconf_lock, datastore="candidate", operation="unlock", manager=task.host["manager"])


def main():
    """Execute Nornir Script."""
    print_result(west_region.run(task=example_global_lock))
    print_result(west_region.run(task=example_edit_config))
    print_result(west_region.run(task=example_unlock))


if __name__ == "__main__":
    main()
