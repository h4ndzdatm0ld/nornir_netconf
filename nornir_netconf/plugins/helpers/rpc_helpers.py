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


def unpack_rpc(rpc: RPCReply, xmldict: bool = False) -> Dict:
    """Extract RPC attrs of interest.

    Args:
        rpc (RPCReply): RPC Reply from Netconf Server
        xmldict (boolean): convert xml to dict

    Return:
        Dict: "RPC Attributes"
    """
    result = {
        "error": rpc.error,
        "errors": rpc.errors,
        "ok": rpc.ok,
        "rpc": rpc,
    }

    if xmldict:
        result["xml_dict"] = xml_to_dict(rpc)

    return result


def get_result(rpc: Union[RPCReply, Dict], xmldict: bool = False) -> Dict:
    """Check if RPC reply is valid and unpack.

    Args:
        rpc (Union[RPCReply, Dict]): RPC Reply from Netconf Server or Dict
        xmldict (boolean): convert xml to dict

    Returns:
        Dict: Results dict to expand in Result object
    """
    # The RPCReply may vary in attributes it contains within the object. Sometimes, the 'ok' response
    # could be missing as well as the 'data_xml'. All conform to the standard 'get_result'
    # dictionary expected by the user.
    result = {"ok": {}, "error": {}, "errors": {}}

    if any(i for i in dir(rpc) if i == "ok"):
        if rpc.ok:
            return {"failed": False, "result": unpack_rpc(rpc, xmldict)}
        try:
            if rpc.data_xml:
                result["rpc"] = rpc
                result["ok"] = True
                if xmldict:
                    result["xml_dict"] = xml_to_dict(rpc)
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
