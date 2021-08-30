"""Nornir Netconf Tasks."""
from .netconf_capabilities import netconf_capabilities
from .netconf_edit_config import netconf_edit_config
from .netconf_get import netconf_get
from .netconf_get_config import netconf_get_config
from .netconf_lock import netconf_lock

__all__ = (
    "netconf_capabilities",
    "netconf_edit_config",
    "netconf_get",
    "netconf_get_config",
    "netconf_lock",
)
