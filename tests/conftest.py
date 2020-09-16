import os

from nornir import InitNornir

import pytest


@pytest.fixture
def nornir(request):
    """Initializes nornir, and close connections after tests"""
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {"host_file": f"{dir_path}/inventory_data/hosts.yaml"},
        },
        logging={"enabled": False},
        dry_run=True,
    ) as nornir:
        yield nornir
