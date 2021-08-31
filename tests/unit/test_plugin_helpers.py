"""Test Helper functions."""
from nornir_netconf.plugins.helpers import get_result
from unittest import mock
import ncclient


@mock.patch.object(ncclient.operations.rpc, "RPCReply")
def test_get_result(rpc_reply):
    """Test get result failed."""
    rpc_reply.ok = False
    result = get_result(rpc_reply)
    assert result == {"failed": True, "result": {}}
