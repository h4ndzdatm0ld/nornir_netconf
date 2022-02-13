# How to use the `Examples` directory

The Examples directory contains a project folder that's setup to quickly test some functionalities of Nornir Netconf Plugin. This presents the users the ability to execute tasks and see how the plugin responds.

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
(nornir-netconf-Ky5gYI2O-py3.9) ➜  example-project git:(sros-integration) ✗ python nr_get_config.py
example_netconf_get_config******************************************************
* nokia_rtr ** changed : False *************************************************
vvvv example_netconf_get_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
<?xml version="1.0" encoding="UTF-8"?><rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:c0be66a3-5d67-4ef4-856e-a8c9c56c77a8">
    <data>
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <router>
                <router-name>Base</router-name>
                <interface>
                    <interface-name>L3-OAM-eNodeB069420-W1</interface-name>
                    <admin-state>disable</admin-state>
                    <ingress-stats>false</ingress-stats>
                </interface>
            </router>
        </configure>
    </data>
</rpc-reply>
---- netconf_get_config ** changed : False ------------------------------------- INFO
{ 'error': {},
  'errors': [],
  'ok': None,
  'rpc': <ncclient.xml_.NCElement object at 0x7f2c04381070>}
```
