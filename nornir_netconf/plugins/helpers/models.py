"""Data Models."""
from dataclasses import dataclass, field
from typing import List, Optional

from ncclient.manager import Manager
from ncclient.operations.rpc import RPCReply


@dataclass
class RpcResult:
    """RPC Reply Result Model."""

    rpc: Optional[RPCReply] = field(default=None, repr=True)
    manager: Optional[Manager] = field(default=None, repr=False)


@dataclass
class SchemaResult:
    """Get Schema Result."""

    directory: str = field(repr=True)
    errors: List[str] = field(repr=False, default_factory=list)
    files: List[str] = field(repr=False, default_factory=list)
