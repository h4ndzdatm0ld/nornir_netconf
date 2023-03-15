# DataClasses Implementation

As of version 2.0, there will be an introduction of `RpcResult` and `SchemaResult`. Going forward, any task will return a dataclass to ensure a good experience for the developers and users of this project.

Please view the source code to ensure this is the most update to date information on the implementations.

> SOURCE: `nornir_netconf/plugins/helpers/rpc.py`

## RpcResult

This will be the object that will mostly be presented back to users as the return value to the `Result.result` attribute.

```python
@dataclass
class RpcResult:
    """RPC Reply Result Model."""

    rpc: Optional[RPCReply] = field(default=None, repr=True)
    manager: Optional[Manager] = field(default=None, repr=False)
```

## SchemaResult

This will provide users with information about valid schemas which were created and in what `files` they were outputted to. Additionally, the `directory` in which the files where aggregated and written to. if any errors were encountered during the writing of the files or retrieval of the schema, they will be aggregated into the `errors` attribute.

```python
@dataclass
class SchemaResult:
    """Get Schema Result."""

    directory: str = field(repr=True)
    errors: List[str] = field(repr=False, default_factory=list)
    files: List[str] = field(repr=False, default_factory=list)
```
