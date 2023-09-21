#!/usr/bin/env python3

"""
Script: configure_via_api.py
Author: Viacheslav Hletenko
Date: 2023
Description:
Configure VyOS via API
Add configiration to file config.conf

Requires VyOS API configuration:

set service https api keys id KID key 'foo'
set service https api socket

Usage: python3 configure_via_api.py
"""

import json
import re

import requests
import urllib3


def convert_to_json_commands(input_str):
    """
    Convert a multiline string of commands into a JSON representation.

    Args:
        input_str (str): A multiline string containing commands.

    Returns:
        str: A JSON string representing the commands in a structured format.
    """
    commands = input_str.strip().split('\n')
    result = []

    for command in commands:
        # Use regular expressions to extract parts based on desired pattern
        parts = re.findall(r"[^\s']+|'[^']+'", command)
        path = [part.replace("'", "") for part in parts[1:]]
        operation = {"op": "set", "path": path}
        result.append(operation)

    return json.dumps(result, indent=4)


def configure_vyos(address, key, data):
    """
    Configure a VyOS device using the provided data.

    Args:
        address (str): The address of the VyOS device.
        key (str): The key for authentication.
        data (str): The configuration data to be applied.

    Returns:
        None

    Raises:
        Exception: If the configuration fails.
    """
    headers = {}
    url = f'https://{address}/configure'
    payload = {'data': data, 'key': key}

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.post(url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        print("Configuration successful.")
        print(f"VyOS host '{address}' configured.")
    else:
        print("Configuration failed. Status code:", response.status_code)
        print("Response:", response.text)


if __name__ == '__main__':

    # Set VyOS host address and API key
    vyos_host = '192.168.122.14'
    vyos_api_key = 'foo'

    # Read configuration from config.conf
    with open('config.conf', 'r') as file:
        commands = file.read()

    config_json = convert_to_json_commands(commands)

    configure_vyos(address=vyos_host, key=vyos_api_key, data=config_json)
