"""Netconf Connection Plugin."""
from typing import Any, Dict, Optional

from ncclient import manager
from nornir.core.configuration import Config

from nornir_netconf.plugins.helpers import check_file

CONNECTION_NAME = "netconf"


class Netconf:
    """This plugin connects to the device via NETCONF using ncclient library.

    Inventory:
        extras: See
        `here <https://ncclient.readthedocs.io/en/latest/transport.html#ncclient.transport.SSHSession.connect>`_
    Example on how to configure a device to use netconfig without using an ssh agent and without verifying the keys::
        ---
        nc_device:
            hostname: 192.168.16.20
            username: admin
            password: admin
            port: 2022
            connection_options:
                netconf:
                    extras:
                        allow_agent: False
                        hostkey_verify: False
    Then it can be used like::
        >>> from nornir import InitNornir
        >>> from nornir.core.task import Result, Task
        >>>
        >>> nr = InitNornir(
        >>>    inventory={
        >>>        "options": {
        >>>            "hosts": {
        >>>                "rtr00": {
        >>>                    "hostname": "localhost",
        >>>                    "username": "admin",
        >>>                    "password": "admin",
        >>>                    "port": 65030,
        >>>                    "platform": "whatever",
        >>>                    "connection_options": {
        >>>                        "netconf": {"extras": {"hostkey_verify": False}}
        >>>                    },
        >>>                }
        >>>           }
        >>>        }
        >>>    }
        >>>)
        >>>
        >>>
        >>> def netconf_code(task: Task) -> Result:
        >>>    manager = task.host.get_connection("netconf", task.nornir.config)
        >>>
        >>>    # get running config and system state
        >>>    print(manager.get())
        >>>
        >>>    # get only hostname
        >>>    print(manager.get(filter=("xpath", "/sys:system/sys:hostname")))
        >>>
        >>>    # get candidate config
        >>>    print(manager.get_config("candidate"))
        >>>
        >>>    # lock
        >>>    print(manager.lock("candidate"))
        >>>
        >>>    # edit configuration
        >>>    res = manager.edit_config(
        >>>        "candidate",
        >>>        "<sys:system><sys:hostname>asd</sys:hostname></sys:system>",
        >>>        default_operation="merge",
        >>>    )
        >>>    print(res)
        >>>
        >>>    print(manager.commit())
        >>>
        >>>    # unlock
        >>>    print(manager.unlock("candidate"))
        >>>
        >>>    return Result(result="ok", host=task.host)
        >>>
        >>>
        >>> nr.run(task=netconf_code)
    """  # noqa

    def open(
        self,
        hostname: Optional[str],
        username: Optional[str],
        password: Optional[str],
        port: Optional[int],
        platform: Optional[str],
        extras: Optional[Dict[str, Any]] = None,
        configuration: Optional[Config] = None,
    ) -> None:
        """Open NETCONF connection."""
        extras = extras or {}

        parameters: Dict[str, Any] = {
            "host": hostname,
            "username": username,
            "password": password,
            "port": port or 830,
        }

        if platform:
            parameters["device_params"] = {"name": platform}

        ssh_config_file = extras.get("ssh_config", configuration.ssh.config_file)  # type: ignore[union-attr]
        if check_file(ssh_config_file):
            parameters["ssh_config"] = ssh_config_file

        parameters.update(extras)
        self.connection = manager.connect_ssh(**parameters)  # pylint: disable=W0201

    def close(self) -> None:
        """Close."""
        self.connection.close_session()
