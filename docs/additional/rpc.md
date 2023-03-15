# Key Differences in RPC response objects

Different vendor implementations return back different attributes in the RPC response.

The `ok` response is not always a present attribute, unfortunately. The `data_xml` or `xml` attribute could be parsed to find this XML representation at times

The `rpc` attribute that's part of the `Result.RpcResult` response object is the actual RPC response from the server.

Lets compare the attributes from an `SROS`device and a `Cisco IOSXR` device. The following shows the attributes and the type for the RPC object.

`Nokia SROS 7750`

```py
['_NCElement__doc', '_NCElement__huge_tree', '_NCElement__result', '_NCElement__transform_reply', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'data_xml', 'find', 'findall', 'findtext', 'remove_namespaces', 'tostring', 'xpath']

<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:c5edead4-b47f-4f5f-a82c-d8a54ebcb901">
  <ok/>
</rpc-reply>

<class 'ncclient.xml_.NCElement'>
```

`Cisco IOSxR`

```py
['ERROR_CLS', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_errors', '_huge_tree', '_parsed', '_parsing_error_transform', '_parsing_hook', '_raw', '_root', 'error', 'errors', 'ok', 'parse', 'set_parsing_error_transform', 'xml']
<?xml version="1.0"?>
<rpc-reply message-id="urn:uuid:66b9fc57-bfa8-4ace-a847-86cc9a99ea4b" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
 <ok/>
</rpc-reply>

<class 'ncclient.operations.rpc.RPCReply'>
```

Hopefully this helps understand the differences in some RPC responses.
