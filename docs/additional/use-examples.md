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
