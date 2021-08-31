"""Helper to extract info from RPC reply."""
from typing import Dict

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


def get_result(rpc: RPCReply) -> Dict:
    """Check if RPC reply is valid and unpack.

    Args:
        rpc (RPCReply): RPC Reply from Netconf Server

    Returns:
        Dict: Results dict to expand in Result object
    """
    try:
        if rpc.ok:
            return {"failed": False, "result": unpack_rpc(rpc)}
    except AttributeError:
        try:
            if rpc.data_xml:
                result = {"error": {}, "errors": {}, "ok": {}, "rpc": rpc, "xml_dict": xml_to_dict(rpc)}
                return {"failed": False, "result": result}
        except AttributeError:
            return {"failed": True, "result": {}}
    return {"failed": True, "result": {}}
