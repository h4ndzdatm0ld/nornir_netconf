"""Nornir NETCONF Plugin."""
try:
    from importlib import metadata  # type: ignore
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata  # type: ignore

# This will read version from pyproject.toml
__version__ = metadata.version("nornir_netconf")
