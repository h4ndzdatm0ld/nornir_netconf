# Nornir NETCONF

[![codecov](https://codecov.io/gh/h4ndzdatm0ld/nornir_netconf/branch/develop/graph/badge.svg?token=MRI39YHOOR)](https://codecov.io/gh/h4ndzdatm0ld/nornir_netconf)
[![Build Status](https://github.com/nornir-automation/nornir_netconf/workflows/test_nornir_netconf/badge.svg)](https://github.com/nornir-automation/nornir_netconf/actions?query=workflow%3Atest_nornir_netconf)

Collection of NETCONF tasks and connection plugin for [Nornir](https://github.com/nornir-automation/nornir)

## Documentation

Documentation is generated with Sphinx and hosted with Github Pages. [Documentation](https://h4ndzdatm0ld.github.io/nornir_netconf/)

To generate the latest documentation locally:

```bash
sphinx-build -vvv -b html ./docs ./docs/public
cd docs/public
python -m http.server
```

## Installation

------------

```bash
pip install nornir_netconf
```

## Plugins

------------

### Connections

------------

* **netconf** - Connect to network devices using [ncclient](https://github.com/ncclient/ncclient)

### Tasks

------------

* **netconf_capabilities** - Return server capabilities from target
* **netconf_get** - Returns state data based on the supplied xpath
* **netconf_get_config** - Returns configuration from specified configuration store (default="running")
* **netconf_edit_config** - Edits configuration on specified datastore (default="running")
* **netconf_lock** - Locks or Unlocks a specified datastore (default="lock")
* **netconf_commit** - Commits a change

## Response Result

The goal of the task results is to put the NETCONF RPC-reply back in your hands. An 'rpc' key will be available which can then be used to access 'data_xml' or 'xml' depending on the type of response or any other attributes available, such as 'error', 'errors'. Some of the RPC is unpacked and provided back as part of the Result by default, including the 'error', 'errors' and 'ok' if available. Anything else can be accessed directly from the rpc.

Furthermore, some tasks allow the 'xml_dict' boolean argument. This will take the response RPC XML and convert it into a python dictionary. Keep in mind, this may not be perfect as XML does't quite translate 100% into a python dictionary.

For example, an xml response can include a collapsed response with open/close as so:  ```<ok/>```
If parsed into python dictionary using xml_dict argument, the key of 'ok' will have a value of none.  However, if we were to be parsing ```<enabled>True</enabled>``` this would show a key of 'enabled' and a value of 'True'.

This is a simple built-in solution available, but not the only one. You have the RPC as part of the response and you are able to parse it anyway or method which works better for you.

## Global Lock

The `netconf_lock` task will always return the Manager object, which is the established (and locked) agent used to send RPC's back and forth. The idea of retrieving the Manager is to carry this established locked session from task to task and only lock and unlock once during a run of tasks.  Please review the examples below to see how to extract the manager and store it under the `task.host` dictionary as a variable which can be used across multiple tasks. The Manager is passed into other tasks and re-used to send RPCs to the remote server.

### Examples

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

Below is the snippet of a host inside the host-local.yml file and it's associated group, 'sros'.

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
from nornir_utils.plugins.functions import print_result
from nornir_netconf.plugins.tasks import netconf_get_config


__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by 'west-region' assignment
west_region = nr.filter(region="west-region")


def example_netconf_get_config(task):
    """Test get config."""

    task.run(
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


def main():
    """Execute Nornir Script."""
    print_result(west_region.run(task=example_netconf_get_config))


if __name__ == "__main__":
    main()

```

</details>

<details><summary>Task: Get Capabilities</summary>

```python
"""Nornir NETCONF Example Task: 'get-config'."""
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netconf.plugins.tasks import netconf_capabilities


__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by 'west-region' assignment
west_region = nr.filter(region="west-region")


def example_netconf_get_capabilities(task):
    """Test get capabilities."""
    task.run(netconf_capabilities)


def main():
    """Execute Nornir Script."""
    print_result(west_region.run(task=example_netconf_get_capabilities))


if __name__ == "__main__":
    main()
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
    task.host["manager"] = lock.result["manager"]


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
        netconf_edit_config, config=config_payload, target="candidate", manager=task.host["manager"], xmldict=True
    )

    # Access the RPC response object directly.
    # Or you can check the 'ok' attr from an rpc response as well, if it exists.
    if "ok" in result.result["rpc"].data_xml:
        task.run(netconf_commit, manager=task.host["manager"], xmldict=True)

    # Check OK key exists, as we passed in 'xmldict=True'
    print(result.result["xml_dict"].keys())

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

### Additional Documentation

* [NCClient](https://ncclient.readthedocs.io/en/latest/)
* [Sysrepo](https://www.sysrepo.org/)

## Contributions

------------

No line of code shall go un tested! Any contribution will need to be accounted by the coverage report and satisfy all linting.

Linters:

* Fake8
* Black
* Yamllint
* Pylint
* Pydocstyle
* Bandit
* MyPy

### Testing

To test within a local docker environment

```bash
git clone https://github.com/h4ndzdatm0ld/nornir_netconf
```

```bash
docker-compose build && docker-compose run test
```

To test locally with pytest

```bash
docker-compose up netconf1
```

```bash
poetry install && poetry shell
```

```bash
pytest --cov=nornir_netconf --color=yes --disable-pytest-warnings -vvv
```

### Integration Tests

Devices with full integration tests (Eve-NG)

* Nokia SROS - TiMOS-C -20.5.R2
* Cisco IOSxR - 6.3.1

Devices testing against Always-ON Sandboxes (Cisco DevNet)

* ios-xe - Cisco IOS XE Software, Version 17.03.01a
* ios-xr - ( Pending )

These tests are ran locally against an EVE-NG environment. At the moment, there is no solution to run these integration tests within the Github Actions CI.

### Sysrepo: netopeer2

Majority of integration tests are ran against a docker instance of [netopeer2](https://hub.docker.com/r/sysrepo/sysrepo-netopeer2)

From the [Sysrepo](https://www.sysrepo.org/) website:

"Netopeer2 and Sysrepo provide a fully open source and standards compliant implementation of a NETCONF server and YANG configuration data stores."
