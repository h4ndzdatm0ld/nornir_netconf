"""Netconf Connection Plugin."""
from nornir_netconf.plugins.connections.netconf import Netconf
from nornir_netconf.plugins.connections.netconf import CONNECTION_NAME

__all__ = ("Netconf", "CONNECTION_NAME")
