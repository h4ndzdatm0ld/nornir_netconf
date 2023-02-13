"""Helper to extract info from RPC reply."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from ncclient.operations.rpc import RPCReply


def check_capability(capabilities: List[str], capability: str) -> bool:
    """Evaluate capabilities and return True if capability is available."""
    return any(True for cap in capabilities if capability in cap)


@dataclass
class RpcResult:
    """Normalize RPC and NCCelement responses."""

    ok: bool = field(default=False, repr=False)
    error: Optional[str] = field(default=None, repr=False)
    errors: Optional[List[str]] = field(default_factory=list, repr=False)
    xml: Optional[str] = field(default=None, repr=False)
    rpc: Optional[RPCReply] = field(default=None, repr=False)


def unpack_rpc(rpc: RPCReply) -> Dict[str, Union[RPCReply, str]]:
    """Extract RPC attrs of interest.

    Args:
        rpc (RPCReply): RPC Reply from Netconf Server

    Return:
        Dict: "RPC Attributes"
    """
    result = {
        "error": rpc.error,
        "errors": rpc.errors,
        "ok": rpc.ok,
        "rpc": rpc,
    }

    return result


def get_result(rpc: Union[RPCReply, Dict[str, Any]]) -> Dict[str, Union[RPCReply, str]]:
    """Check if RPC reply is valid and unpack.

    Args:
        rpc (Union[RPCReply, Dict]): RPC Reply from Netconf Server or Dict

    Returns:
        Dict: Results dict to expand in Result object
    """
    # The RPCReply may vary in attributes it contains within the object. Sometimes, the 'ok' response
    # could be missing. In order to standardize a similar result we evaluate the response and
    # make adjustment where necessary to keep responses somewhat consistent without assumptions.

    result: Dict[str, Any] = {"error": {}, "errors": []}
    if not isinstance(rpc, Dict):
        # RPC will either have 'ok' or 'data_xml' attr:
        if any(i for i in dir(rpc) if i in ["ok", "data_xml"]):
            try:
                if rpc.ok:
                    failed = False
                else:
                    failed = True
                return {"failed": failed, "result": unpack_rpc(rpc)}
            except AttributeError:
                # Re-create `unpack_rpc` output keys to keep consistency.
                result["rpc"] = rpc
                result["ok"] = True if "<ok/>" in rpc.data_xml else None
                return {"failed": False, "result": result}

    # TODO = This is failing 1 test. THis needs to go.
    # Safe to say, at this point the replies are not RPC or NCElements.
    # So we can take advantage of passing dictionaries in and safe gets.
    if isinstance(rpc, Dict):
        result["error"] = rpc.get("error", {})
        result["errors"] = rpc.get("errors", "Unable to find 'ok' or data_xml in response object.")
        result["ok"] = rpc.get("ok", False)
        result["rpc"] = rpc.get("rpc", {})
    return {"failed": True, "result": result}
