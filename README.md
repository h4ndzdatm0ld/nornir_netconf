# Nornir NETCONF

[![codecov](https://codecov.io/gh/h4ndzdatm0ld/nornir_netconf/branch/develop/graph/badge.svg?token=MRI39YHOOR)](https://codecov.io/gh/h4ndzdatm0ld/nornir_netconf)
[![Build Status](https://github.com/nornir-automation/nornir_netconf/workflows/test_nornir_netconf/badge.svg)](https://github.com/nornir-automation/nornir_netconf/actions?query=workflow%3Atest_nornir_netconf)

Collection of NETCONF tasks and connection plugin for [Nornir](https://github.com/nornir-automation/nornir)

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
* **netconf_lock** - Locks a specified datastore
* **netconf_commit** - Commits a change

### Documentation

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
poetry install && poetry shell
```

```bash
pytest --cov=nornir_netconf --color=yes --disable-pytest-warnings -vvv
```

### Integration Tests

There are currently two different vendors that have full integration tests.

* Nokia SROS
* Cisco IOSxR (Pending)

These tests are ran locally against an EVE-NG environment. At the moment, there is no solution to run these integration tests within the Github Actions CI.

### Sysrepo: netopeer2

Majority of integration tests are ran against a docker instance of [netopeer2](https://hub.docker.com/r/sysrepo/sysrepo-netopeer2)

From the [Sysrepo](https://www.sysrepo.org/) website:

"Netopeer2 and Sysrepo provide a fully open source and standards compliant implementation of a NETCONF server and YANG configuration data stores."
