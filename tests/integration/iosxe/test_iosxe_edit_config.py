"""Integration test against IOSXE device."""
from nornir_utils.plugins.functions import print_result

from nornir_netconf.plugins.tasks import netconf_edit_config
from tests.conftest import skip_integration_tests, xml_dict

DEVICE_NAME = "iosxe_rtr"
