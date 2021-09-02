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
* **netconf_lock** - Locks a datastore

### Documentation

* [NCClient](https://ncclient.readthedocs.io/en/latest/)
