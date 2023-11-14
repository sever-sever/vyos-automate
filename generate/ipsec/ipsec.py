#!/usr/bin/env python3

"""
Script: vyos_firewall.py
Author: Viacheslav Hletenko
Date: 2023
Description:
Generate IPSec VyOS configuration. Variables are defined in config.yaml

Usage: python3 ipsec.py > vyos_ipsec.conf
"""

import yaml
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template


def generate_config(config: dict, template: Template) -> str:
    """
    Generate VyOS config rules based on the dictionary configuration.

    Args:
        config (dict): A dictionary generated from config.yaml.
        template (jinja2.Template): A Jinja2 template used for generating config.

    Returns:
        str: The generated config as a string.
    """
    return template.render(config)


if __name__ == "__main__":
    with open("config.yaml", "r", encoding="utf-8") as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)

    env = Environment(loader=FileSystemLoader("templates"), trim_blocks=True)

    ipsec = env.get_template("ipsec.j2")
    print(generate_config(conf, ipsec))
