# type: ignore
"""Nornir NETCONF Example Task: 'edit-config', 'netconf_lock'."""
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import (
    netconf_commit,
    netconf_edit_config,
    netconf_lock,
)

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by 'west-region' assignment
west_region = nr.filter(region="west-region")


def example_global_lock(task):
    """Test global lock operation of 'candidate' datastore."""
    lock = task.run(netconf_lock, datastore="candidate", operation="lock")
    # Retrieve the Manager(agent) from lock operation and store for further
    # operations.
    task.host["manager"] = lock.result["manager"]


def example_edit_config(task):
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

    result = task.run(netconf_edit_config, config=config_payload, target="candidate", manager=task.host["manager"])

    # Access the RPC response object directly.
    # Or you can check the 'ok' attr from an rpc response as well, if it exists.
    if "ok" in result.result["rpc"].data_xml:
        task.run(netconf_commit, manager=task.host["manager"])


def example_unlock(task):
    """Unlock candidate datastore."""
    task.run(netconf_lock, datastore="candidate", operation="unlock", manager=task.host["manager"])


def main():
    """Execute Nornir Script."""
    print_result(west_region.run(task=example_global_lock))
    print_result(west_region.run(task=example_edit_config))
    print_result(west_region.run(task=example_unlock))


if __name__ == "__main__":
    main()
