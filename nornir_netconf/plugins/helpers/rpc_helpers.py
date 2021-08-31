"""Helper to extract info from RPC reply."""
from typing import Dict, Union

import xmltodict
from ncclient.operations.rpc import RPCReply


def xml_to_dict(rpc: RPCReply) -> Dict:
    """Convert XML from RPC reply to dict.

    Args:
        rpc (RPCReply): RPC Reply from Netconf Server

    Returns:
        Dict: xml response -> Dict
    """
    try:
        return xmltodict.parse(rpc.data_xml)
    except Exception as err_ex:
        return {"error": f"Unable to parse XML to Dict. {err_ex}."}


def unpack_rpc(rpc: RPCReply) -> Dict:
    """Extract RPC attrs of interest.

    Args:
        rpc (RPCReply): RPC Reply from Netconf Server

    Return:
        Dict: "RPC Attributes"
    """
    return {"error": rpc.error, "errors": rpc.errors, "ok": rpc.ok, "rpc": rpc, "xml_dict": xml_to_dict(rpc)}


def get_result(rpc: Union[RPCReply, Dict]) -> Dict:
    """Check if RPC reply is valid and unpack.

    Args:
        rpc (RPCReply): RPC Reply from Netconf Server

    Returns:
        Dict: Results dict to expand in Result object
    """
    # These try blocks are to handle RPCReply that vary. Sometimes, the 'ok' response
    # could be missing as well as the 'data_xml'. All conform to the standard 'get_result'
    # dictionary expected by the user.
    result = {"ok": {}, "error": {}, "errors": {}}

    try:
        if rpc.ok:
            return {"failed": False, "result": unpack_rpc(rpc)}
    except AttributeError:
        pass

    try:
        if rpc.data_xml:
            result["xml_dict"] = xml_to_dict(rpc)
            result["ok"] = True
            return {"failed": False, "result": result}
    except AttributeError:
        pass

    # Safe to say, at this point the replies are not RPC or NCElements.
    # So we can take advantage of passing dictionaries in and safe gets.
    if isinstance(rpc, Dict):
        result["error"] = rpc.get("error", {})
        result["errors"] = rpc.get("errors", "Unable to find 'ok' or data_xml in response object.")
        result["ok"] = rpc.get("ok", False)
        result["rpc"] = rpc.get("rpc", {})
        result["xml_dict"] = rpc.get("xml_dict", {})

    return {"failed": True, "result": result}
