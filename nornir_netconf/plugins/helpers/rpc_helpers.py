"""Helper to extract info from RPC reply."""
from typing import Dict
from ncclient.operations.rpc import RPCReply


def unpack_rpc(rpc: RPCReply) -> Dict:
    """Extract RPC attrs of interest.

    Args:
        rpc (RPCReply): RPC Reply from Netconf Server

    Return:
        Dict: "RPC Attributes"
    """
    return {"error": rpc.error, "errors": rpc.errors, "ok": rpc.ok, "rpc": rpc}
