# How to use the `Examples` directory

The `examples` directory contains a project folder that's setup to quickly test some functionalities of `NORNIR Netconf` Plugin. This presents the users and/or developers the ability to execute tasks and see how the plugin responds. However, this plugin has tons of tests so feel free to experiment.

Start the ContainerLab Nodes.

```bash
docker-compose up -d
```

Install the project locally

```bash
poetry install
```

Activate

```bash
poetry shell
```

From the `examples-project` directory, execute a script against the Nokia SROS device.

```bash
(nornir-netconf-Ky5gYI2O-py3.9) ➜  example-project git:(sros-integration) ✗ pwd
/home/htinoco/Dropbox/py-progz/nornir_plugins/nornir_netconf/examples/example-project
```

```bash
(nornir-netconf-Ky5gYI2O-py3.10) ➜  example-project git:(feat/docs/update) ✗ python3 nr_get_config.py 
example_netconf_get_config******************************************************
* nokia_rtr ** changed : False *************************************************
vvvv example_netconf_get_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
<?xml version="1.0" encoding="UTF-8"?><rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:16c59796-e4c7-4702-9956-7b3988bb68ff">
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
RpcResult(rpc=<ncclient.xml_.NCElement object at 0x7f780997a080>)
^^^^ END example_netconf_get_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(nornir-netconf-Ky5gYI2O-py3.10) ➜  example-project git:(feat/docs/update) ✗ 
```
