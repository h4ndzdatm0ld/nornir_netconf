# type: ignore
"""Get Schemas from NETCONF device."""
from nornir import InitNornir
from nornir.core import Task
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import netconf_get, netconf_get_schemas
from tests.conftest import xml_dict

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")


# Filter the hosts by 'west-region' assignment
west_region = nr.filter(region="west-region")

SCHEMA_FILTER = """
<netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
    <schemas>
    </schemas>
</netconf-state>
"""


def example_task_get_schemas(task: Task) -> Result:
    """Get Schemas from NETCONF device."""
    result = task.run(netconf_get, path=SCHEMA_FILTER, filter_type="subtree")
    # xml_dict is a custom function to convert XML to Python dictionary. Not part of Nornir Plugin.
    # See the code example if you want to use it.
    parsed = xml_dict(result.result.rpc.data_xml)
    first_schema = parsed["rpc-reply"]["data"]["netconf-state"]["schemas"]["schema"][0]
    return task.run(netconf_get_schemas, schemas=[first_schema["identifier"]], schema_path="./output/schemas")


def main():
    """Execute Nornir Script."""
    print_result(west_region.run(task=example_task_get_schemas))


if __name__ == "__main__":
    main()
