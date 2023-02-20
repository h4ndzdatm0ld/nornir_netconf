"""Helper to extract info from RPC reply."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from ncclient.manager import Manager
from ncclient.operations.rpc import RPCReply


def check_capability(capabilities: List[str], capability: str) -> bool:
    """Evaluate capabilities and return True if capability is available."""
    return any(True for cap in capabilities if capability in cap)


@dataclass
class RpcResult:
    """RPC Reply Result Model."""

    rpc: Optional[RPCReply] = field(default=None, repr=False)
    manager: Optional[Manager] = field(default=None, repr=False)
    error: Optional[str] = field(default=None, repr=False)
