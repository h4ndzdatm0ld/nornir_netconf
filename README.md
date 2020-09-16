[![Build Status](https://github.com/nornir-automation/nornir_netconf/workflows/test_nornir_netconf/badge.svg)](https://github.com/nornir-automation/nornir_netconf/actions?query=workflow%3Atest_nornir_netconf)


nornir_netconf
=============

Collection of simple plugins for `nornir <github.com/nornir-automation/nornir/>`_

Installation
------------

```bash
pip install nornir__netconf
```

Plugins
-------

Connections
___________

* **netconf** - Connect to network devices using [ncclient](https://github.com/ncclient/ncclient)

Tasks
_____

* **netconf_capabilities** - Return server capabilities from target
* **netconf_get** - Returns state data based on the supplied xpath
* **netconf_get_config** - Returns configuration from running or specified configuration store
* **netconf_edit_config** - Edits configuration in running or the target configuration store

