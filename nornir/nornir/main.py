#!/usr/bin/env python3

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from pprint import pprint

# nr = InitNornir(config_file="config.yaml")
# rtr = nr.filter(name="r1")
# r = rtr.run(task=napalm_get, getters=["facts"])
#
# # pprint(r["r1"][0].result)
# pprint(r)


def get_device_facts(device_name: str, config_file: str = "config.yaml"):
    """Get the facts of a VyOS using Nornir and Napalm"""
    # Initialize Nornir
    nr = InitNornir(config_file=config_file)

    # Filter the device by name
    device = nr.filter(name=device_name)

    # Run the napalm_get task to get facts
    result = device.run(task=napalm_get, getters=["facts"])

    # return the facts of the device
    return result[device_name][0].result


def get_all_devices_facts(config_file="config.yaml"):
    # Initialize Nornir
    nr = InitNornir(config_file=config_file)

    # Run the napalm_get task to get facts for all devices
    result = nr.run(task=napalm_get, getters=["facts"])

    # return the facts in a dictionary
    return {
        device_name: task_result[0].result
        for device_name, task_result in result.items()
    }


if __name__ == "__main__":
    # Get facts for a single device
    router = "r1"
    facts = get_device_facts(router)
    pprint(facts)

    # Get facts for all devices
    all_facts = get_all_devices_facts()
    pprint(all_facts)

