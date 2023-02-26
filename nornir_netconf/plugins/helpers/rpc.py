"""Helper to extract info from RPC reply."""
from typing import List


def check_capability(capabilities: List[str], capability: str) -> bool:
    """Evaluate capabilities and return True if capability is available."""
    return any(True for cap in capabilities if capability in cap)
