"""Nornir Netconf Tasks.

Operations are separated into their own categorized folder.
"""
from .capabilities.netconf_capabilities import netconf_capabilities
from .editing.netconf_edit_config import netconf_edit_config
from .retrieval.netconf_get import netconf_get
from .retrieval.netconf_get_config import netconf_get_config
from .retrieval.netconf_get_schemas import netconf_get_schemas
from .locking.netconf_locking import netconf_locking

__all__ = (
    "netconf_capabilities",
    "netconf_edit_config",
    "netconf_get",
    "netconf_get_config",
    "netconf_locking",
    "netconf_get_schemas",
)
