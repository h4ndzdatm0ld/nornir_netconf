# type: ignore
"""Nornir NETCONF Plugin."""
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

# This will read version from pyproject.toml
__version__ = metadata.version("nornir_netconf")
