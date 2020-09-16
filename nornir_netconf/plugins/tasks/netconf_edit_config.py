from nornir.core.task import Result, Task

from nornir_netconf.plugins.connections import CONNECTION_NAME


def netconf_edit_config(task: Task, config: str, target: str = "running") -> Result:
    """
    Edit configuration of device using Netconf

    Arguments:
        config: Configuration snippet to apply
        target: Target configuration store

    Examples:

        Simple example::

            > nr.run(task=netconf_edit_config, config=desired_config)

    Returns:
        Result object with the following attributes set:
          * result (``str``): The rpc-reply as an XML string
    """
    manager = task.host.get_connection(CONNECTION_NAME, task.nornir.config)

    result = manager.edit_config(config, target=target)

    return Result(host=task.host, result=result.xml)
