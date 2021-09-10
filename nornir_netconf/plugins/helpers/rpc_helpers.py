"""Helper to extract info from RPC reply."""
from typing import Any, Dict, Union, List

import xmltodict
from ncclient.operations.rpc import RPCReply


def check_capability(capabilities: List[str], capability: str) -> bool:
    """Evaluate capabilities and return True if capability is available."""
    return any(True for cap in capabilities if capability in cap)


def xml_to_dict(rpc: RPCReply) -> Union[Any, Dict[str, str]]:
    """Convert XML from RPC reply to dict.

    Args:
        rpc (RPCReply): RPC Reply from Netconf Server

    Returns:
        Dict: xml response -> Dict
    """
    options = list(dir(rpc))
    if "data_xml" in options:
        try:
            return xmltodict.parse(rpc.data_xml)
        except Exception as err_ex:
            return {"error": f"Unable to parse XML to Dict. {err_ex}."}
    elif "xml" in options:
        try:
            return xmltodict.parse(rpc.xml)
        except Exception as err_ex:
            return {"error": f"Unable to parse XML to Dict. {err_ex}."}
    else:
        return {"error": "Unable to parse XML to Dict. '.xml' or 'data_xml' not found."}


def unpack_rpc(rpc: RPCReply, xmldict: bool = False) -> Dict[str, Union[RPCReply, str]]:
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


def get_result(rpc: Union[RPCReply, Dict[str, Any]], xmldict: bool = False) -> Dict[str, Union[RPCReply, str]]:
    """Check if RPC reply is valid and unpack.

    Args:
        rpc (Union[RPCReply, Dict]): RPC Reply from Netconf Server or Dict
        xmldict (boolean): convert xml to dict

    Returns:
        Dict: Results dict to expand in Result object
    """
    # The RPCReply may vary in attributes it contains within the object. Sometimes, the 'ok' response
    # could be missing. In order to standardize a similar result we evaluate the response and
    # make adjustment where necessary to keep responses somewhat consistent without assumptions.

    result: Dict[str, Any] = {"error": "", "errors": ""}
    if not isinstance(rpc, Dict):
        # RPC will either have 'ok' or 'data_xml' attr:
        if any(i for i in dir(rpc) if i in ["ok", "data_xml"]):
            try:
                if rpc.ok:
                    failed = False
                else:
                    failed = True
                return {"failed": failed, "result": unpack_rpc(rpc, xmldict)}
            except AttributeError:
                # Re-create `unpack_rpc` output keys to keep consistency.
                result["rpc"] = rpc
                if xmldict:
                    result["xml_dict"] = xml_to_dict(rpc)
                return {"failed": False, "result": result}
    # Safe to say, at this point the replies are not RPC or NCElements.
    # So we can take advantage of passing dictionaries in and safe gets.
    if isinstance(rpc, Dict):
        result["error"] = rpc.get("error", {})
        result["errors"] = rpc.get("errors", "Unable to find 'ok' or data_xml in response object.")
        result["ok"] = rpc.get("ok", False)
        result["rpc"] = rpc.get("rpc", {})
        result["xml_dict"] = rpc.get("xml_dict", {})
    return {"failed": True, "result": result}
