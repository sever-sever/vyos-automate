#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: vyos_firewall.py
Author: Viacheslav Hletenko
Date: 2023
Description:
Generate basic VyOS firewall rules. Variables are defined in config.yaml
Change firewall.v4.ssh.port and prefixes in config.yaml

Usage: python3 vyos_basic_firewall.py > vyos_firewall.conf
"""

import yaml
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template


def generate_firewall_rules(config: dict, template: Template) -> str:
    """
    Generate VyOS firewall rules based on the dictionary configuration.

    Args:
        config (dict): A dictionary generated from config.yaml.
        template (jinja2.Template): A Jinja2 template used for generating firewall rules.

    Returns:
        str: The generated firewall rules as a string.
    """
    return template.render(config)


if __name__ == "__main__":
    config = yaml.load(open('config.yaml'), Loader=yaml.FullLoader)

    env = Environment(loader=FileSystemLoader('templates'))
    network_group_v4 = env.get_template('network_group_v4.j2')
    local_v4_rules = env.get_template('local_v4_rules.j2')
    output_v4_rules = env.get_template('output_v4_rules.j2')

    print(generate_firewall_rules(config, network_group_v4))
    print(generate_firewall_rules(config, local_v4_rules))
    print(generate_firewall_rules(config, output_v4_rules))
