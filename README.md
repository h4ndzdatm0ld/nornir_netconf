# Nornir NETCONF

[![codecov](https://codecov.io/gh/h4ndzdatm0ld/nornir_netconf/branch/develop/graph/badge.svg?token=MRI39YHOOR)](https://codecov.io/gh/h4ndzdatm0ld/nornir_netconf) [![CI](https://github.com/h4ndzdatm0ld/nornir_netconf/actions/workflows/ci.yml/badge.svg)](https://github.com/h4ndzdatm0ld/nornir_netconf/actions/workflows/ci.yml)

Collection of NETCONF tasks and connection plugin for [Nornir](https://github.com/nornir-automation/nornir)

## Installation

---

```bash
pip install nornir_netconf
```

## Plugins

---

### Connections

---

- **netconf** - Connect to network devices using [ncclient](https://github.com/ncclient/ncclient)

### Tasks

---

- **netconf_capabilities** - Return server capabilities from target -> `Result.result -> RpcResult`
- **netconf_commit** - Commits a change -> `Result.result -> RpcResult`
- **netconf_edit_config** - Edits configuration on specified datastore (default="running") -> `Result.result -> RpcResult`
- **netconf_get** - Returns state data based on the supplied xpath -> `Result.result -> RpcResult`
- **netconf_get_config** - Returns configuration from specified configuration store (default="running") -> `Result.result -> RpcResult`
- **netconf_get_schemas** - Retrieves schemas and saves aggregates content into a directory with schema output -> `Result.result -> SchemaResult`
- **netconf_lock** - Locks or Unlocks a specified datastore (default="lock") -> `Result.result -> RpcResult`
- **netconf_validate** - Validates configuration datastore. Requires the `validate` capability. -> `Result.result -> RpcResult`

## Response Result

The goal of the task results is to put the NETCONF RPC-reply back in your hands. In most cases, the Nornir `Result.result` attribute will return back a `dataclass` depending on the task operation. It's important that you understand the object you will be working with. Please see the `dataclasses` section below and review the code if you want to see what attributes to expect.

### Dataclasses

> Defined in `nornir_netconf/plugins/helpers/models.py`

- `RpcResult` -> This will return an attribute of `rpc` and `manager`. You will encounter this object in most Nornir `Results` as the return value to the `result` attribute. NETCONF / XML payloads can be overwhelming, especially with large configurations and it's just not efficient or useful to display thousands of lines of code in any result.
- `SchemaResult` -> An aggregation of interesting information when grabbing schemas from NETCONF servers.

## Global Lock

The `netconf_lock` task will always return the Manager object, which is the established (and locked) agent used to send RPC's back and forth. The idea of retrieving the Manager is to carry this established locked session from task to task and only lock and unlock once during a run of tasks. Please review the examples below to see how to extract the manager and store it under the `task.host` dictionary as a variable that can be used across multiple tasks. The Manager is passed into other tasks and re-used to send RPCs to the remote server.

## Examples

Head over to the [Examples directory](https://github.com/h4ndzdatm0ld/nornir_netconf/tree/develop/examples) if you'd like to review the files.

<details><summary>Directory Structure</summary>

```bash
├── example-project
│   ├── config.yml
│   ├── inventory
│   │   ├── groups.yml
│   │   ├── hosts-local.yml
│   │   └── ssh_config
│   ├── logs
│   │   └── nornir.log
│   └── nr-get-config.py
└── README.md
```

</details>

<details><summary>Netconf Connection Plugin</summary>

Below is the snippet of a host inside the host-local.yml file and its associated group, `sros`.

```yaml
nokia_rtr:
  hostname: "192.168.1.205"
  port: 830
  groups:
    - "sros"
```

```yaml
sros:
  username: "netconf"
  password: "NCadmin123"
  port: 830
  platform: "sros"
  connection_options:
    netconf:
      extras:
        hostkey_verify: false
        timeout: 300
        allow_agent: false
        look_for_keys: false
```

</details>

<details><summary>Task: Get Config</summary>

```python
    """Nornir NETCONF Example Task: 'get-config'."""
    from nornir import InitNornir
    from nornir.core.task import Task
    from nornir_utils.plugins.functions import print_result

    from nornir_netconf.plugins.tasks import netconf_get_config

    __author__ = "Hugo Tinoco"
    __email__ = "hugotinoco@icloud.com"

    nr = InitNornir("config.yml")

    # Filter the hosts by 'west-region' assignment
    west_region = nr.filter(region="west-region")


    def example_netconf_get_config(task: Task) -> str:
        """Test get config."""
        config = task.run(
            netconf_get_config,
            source="running",
            path="""
            <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
                <router>
                    <router-name>Base</router-name>
                </router>
            </configure>
            """,
            filter_type="subtree",
        )
        return config.result.rpc.data_xml


    def main():
        """Execute Nornir Script."""
        print_result(west_region.run(task=example_netconf_get_config))


    if __name__ == "__main__":
        main()
```

This returns the following

```bash
    vvvv example_netconf_get_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    <?xml version="1.0" encoding="UTF-8"?><rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:918bf169-523f-4bb0-b00c-c97c01a48ecd">
        <data>
            <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
                <router>
                    <router-name>Base</router-name>
                    <interface>
                        <interface-name>L3-OAM-eNodeB069420-X1</interface-name>
                        <admin-state>disable</admin-state>
                        <ingress-stats>false</ingress-stats>
                    </interface>
                </router>
            </configure>
        </data>
    </rpc-reply>
    ---- netconf_get_config ** changed : False ------------------------------------- INFO
    RpcResult(rpc=<ncclient.xml_.NCElement object at 0x7f4b1e08a440>)
    ^^^^ END example_netconf_get_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    (nornir-netconf-Ky5gYI2O-py3.10) ➜  example-project git:(feature/validate-tasks) ✗ 
```

</details>

<details><summary>Task: Get Capabilities</summary>

```python
    """Nornir NETCONF Example Task: 'capabilities'."""
    from nornir import InitNornir
    from nornir.core.task import Task
    from nornir_utils.plugins.functions import print_result

    from nornir_netconf.plugins.tasks import netconf_capabilities

    __author__ = "Hugo Tinoco"
    __email__ = "hugotinoco@icloud.com"

    nr = InitNornir("config.yml")

    # Filter the hosts by 'west-region' assignment
    west_region = nr.filter(region="west-region")


    def example_netconf_get_capabilities(task: Task) -> str:
        """Test get capabilities."""
        capabilities = task.run(netconf_capabilities)
        # This may be a lot, so for example we'll just print the first one
        return [cap for cap in capabilities.result.rpc][0]


    def main():
        """Execute Nornir Script."""
        print_result(west_region.run(task=example_netconf_get_capabilities))


    if __name__ == "__main__":
        main()
```

This returns the following

```bash
    (nornir-netconf-Ky5gYI2O-py3.10) ➜  example-project git:(feature/validate-tasks) ✗ python3 nr_get_capabilities.py 
    example_netconf_get_capabilities************************************************
    * nokia_rtr ** changed : False *************************************************
    vvvv example_netconf_get_capabilities ** changed : False vvvvvvvvvvvvvvvvvvvvvvv INFO
    urn:ietf:params:netconf:base:1.0
    ---- netconf_capabilities ** changed : False ----------------------------------- INFO
    RpcResult(rpc=<dict_keyiterator object at 0x7f7111328c70>)
    ^^^^ END example_netconf_get_capabilities ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    (nornir-netconf-Ky5gYI2O-py3.10) ➜  example-project git:(feature/validate-tasks) ✗ 
```

</details>

<details><summary>Task: Edit-Config with Global Lock</summary>

```python
    """Nornir NETCONF Example Task: 'edit-config', 'netconf_lock'."""
    from nornir import InitNornir
    from nornir_utils.plugins.functions import print_result
    from nornir_netconf.plugins.tasks import netconf_edit_config, netconf_lock, netconf_commit


    __author__ = "Hugo Tinoco"
    __email__ = "hugotinoco@icloud.com"

    nr = InitNornir("config.yml")

    # Filter the hosts by 'west-region' assignment
    west_region = nr.filter(region="west-region")


    def example_global_lock(task):
        """Test global lock operation of 'candidate' datastore."""
        lock = task.run(netconf_lock, datastore="candidate", operation="lock")
        # Retrieve the Manager(agent) from lock operation and store for further
        # operations.
        task.host["manager"] = lock.result.manager


    def example_edit_config(task):
        """Test edit-config with global lock using manager agent."""

        config_payload = """
        <config>
            <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
                <router>
                    <router-name>Base</router-name>
                    <interface>
                        <interface-name>L3-OAM-eNodeB069420-X1</interface-name>
                        <admin-state>disable</admin-state>
                        <ingress-stats>false</ingress-stats>
                    </interface>
                </router>
            </configure>
        </config>
        """

        result = task.run(
            netconf_edit_config, config=config_payload, target="candidate", manager=task.host["manager"]
        )
        # Validate configuration
        task.run(netconf_validate)
        # Commit
        task.run(netconf_commit, manager=task.host["manager"])

    def example_unlock(task):
        """Unlock candidate datastore."""
        task.run(netconf_lock, datastore="candidate", operation="unlock", manager=task.host["manager"])


    def main():
        """Execute Nornir Script."""
        print_result(west_region.run(task=example_global_lock))
        print_result(west_region.run(task=example_edit_config))
        print_result(west_region.run(task=example_unlock))


    if __name__ == "__main__":
        main()

```

</details>

<details><summary>Task: Get Schemas</summary>

```python
    """Get Schemas from NETCONF device."""
    from nornir import InitNornir
    from nornir.core import Task
    from nornir.core.task import Result
    from nornir_utils.plugins.functions import print_result

    from nornir_netconf.plugins.tasks import netconf_get, netconf_get_schemas
    from tests.conftest import xml_dict

    __author__ = "Hugo Tinoco"
    __email__ = "hugotinoco@icloud.com"

    nr = InitNornir("config.yml")


    # Filter the hosts by 'west-region' assignment
    west_region = nr.filter(region="west-region")

    SCHEMA_FILTER = """
    <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
        <schemas>
        </schemas>
    </netconf-state>
    """


    def example_task_get_schemas(task: Task) -> Result:
        """Get Schemas from NETCONF device."""
        result = task.run(netconf_get, path=SCHEMA_FILTER, filter_type="subtree")
        # xml_dict is a custom function to convert XML to Python dictionary. Not part of Nornir Plugin.
        # See the code example if you want to use it.
        parsed = xml_dict(result.result.rpc.data_xml)
        first_schema = parsed["rpc-reply"]["data"]["netconf-state"]["schemas"]["schema"][0]
        return task.run(netconf_get_schemas, schemas=[first_schema["identifier"]], schema_path="./output/schemas")


    def main():
        """Execute Nornir Script."""
        print_result(west_region.run(task=example_task_get_schemas))


    if __name__ == "__main__":
        main()

```

This returns the following

```bash
    (nornir-netconf-Ky5gYI2O-py3.10) ➜  example-project git:(feature/validate-tasks) ✗ python3 nr_get_schemas.py 
    example_task_get_schemas********************************************************
    * nokia_rtr ** changed : False *************************************************
    vvvv example_task_get_schemas ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- netconf_get ** changed : False -------------------------------------------- INFO
    RpcResult(rpc=<ncclient.xml_.NCElement object at 0x7f36391540d0>)
    ---- netconf_get_schemas ** changed : False ------------------------------------ INFO
    SchemaResult(directory='./output/schemas')
    ^^^^ END example_task_get_schemas ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

</details>

## Additional Documentation

- [NCClient](https://ncclient.readthedocs.io/en/latest/)

## Contributions

> Github actions spins up a Containerlab instance to do full integration tests once linting has been satisfied.

---

No line of code shall go untested! Any contribution will need to be accounted for by the coverage report and satisfy all linting.

Linters:

- Ruff (Flake8/Pydocstyle)
- Black
- Yamllint
- Pylint
- Bandit
- MyPy

## Testing

To test within a local docker environment

```bash
git clone https://github.com/h4ndzdatm0ld/nornir_netconf
```

```bash
docker-compose build && docker-compose run test
```

To test locally with pytest

If you'd like to run integration tests with ContainerLab

```bash
export SKIP_INTEGRATION_TESTS=False
```

```bash
docker-compose up -d
```

```bash
poetry install && poetry shell
```

```bash
pytest --cov=nornir_netconf --color=yes --disable-pytest-warnings -vvv
```

### Integration Tests

Devices with full integration tests with ContainerLab

- Nokia SROS - TiMOS-B-21.2.R1
- Cisco IOSxR - Cisco IOS XR Software, Version 6.1.3
- Cisco IOSXE - Cisco IOS XE Software, Version 17.03.02
- Arista CEOS - 4.28.0F-26924507.4280F (engineering build)

## Documentation

Documentation is generated with Sphinx and hosted with Github Pages. [Documentation](https://h4ndzdatm0ld.github.io/nornir_netconf/)
