"""Data Models."""
from dataclasses import dataclass, field
from typing import List, Optional

from ncclient.manager import Manager
from ncclient.operations.rpc import RPCReply


@dataclass
class RpcResult:
    """RPC Reply Result Model."""

    rpc: Optional[RPCReply] = field(default=None, repr=False)
    manager: Optional[Manager] = field(default=None, repr=False)


@dataclass
class SchemaResult:
    """Get Schema Result."""

    errors: Optional[List[str]] = field(default=None, repr=False)
    files: Optional[List[str]] = field(default=None, repr=False)
    directory: Optional[str] = field(default=None, repr=True)
