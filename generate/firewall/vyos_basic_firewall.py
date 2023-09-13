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
from jinja2 import Template

# Template for network groups
network_group_v4 = Template("""
set firewall group network-group {{ firewall.v4.bogon.network_group }} description '{{ firewall.v4.bogon.description }}'
{% for prefix in firewall.v4.bogon.prefixes -%}
set firewall group network-group {{ firewall.v4.bogon.network_group }} network {{ prefix }}
{% endfor -%}

set firewall group network-group {{ firewall.v4.ssh.network_group }} description '{{ firewall.v4.ssh.description }}'
{% for prefix in firewall.v4.ssh.prefixes -%}
set firewall group network-group {{ firewall.v4.ssh.network_group }} network {{ prefix }}
{%- endfor %}
""")

# Template for local rules
local_v4_rules = Template("""
# Input rules
set firewall ipv4 input filter default-action '{{ firewall.v4.input.default_action }}'
{% set seq = firewall.v4.input.seq %}

set firewall ipv4 input filter rule {{ seq.loopback }} description 'Allow loopback'
set firewall ipv4 input filter rule {{ seq.loopback }} action 'accept'
set firewall ipv4 input filter rule {{ seq.loopback }} inbound-interface interface-name 'lo'
set firewall ipv4 input filter rule {{ seq.loopback }} source address '127.0.0.0/8'

set firewall ipv4 input filter rule {{ seq.invalid_tcp_mss_drop }} description 'Drop incorrect TCP MSS sizes'
set firewall ipv4 input filter rule {{ seq.invalid_tcp_mss_drop }} action 'drop'
set firewall ipv4 input filter rule {{ seq.invalid_tcp_mss_drop }} protocol 'tcp'
set firewall ipv4 input filter rule {{ seq.invalid_tcp_mss_drop }} tcp flags syn
set firewall ipv4 input filter rule {{ seq.invalid_tcp_mss_drop }} tcp mss '1-500'

set firewall ipv4 input filter rule {{ seq.stateful }} description 'Allow established/related'
set firewall ipv4 input filter rule {{ seq.stateful }} action 'accept'
set firewall ipv4 input filter rule {{ seq.stateful }} state established 'enable'
set firewall ipv4 input filter rule {{ seq.stateful }} state related 'enable'

set firewall ipv4 input filter rule {{ seq.stateful_drop }} description 'Drop packets with state invalid'
set firewall ipv4 input filter rule {{ seq.stateful_drop }} action 'drop'
set firewall ipv4 input filter rule {{ seq.stateful_drop }} state invalid 'enable'

set firewall ipv4 input filter rule {{ seq.icmp_request }} description 'Allow ICMP requests'
set firewall ipv4 input filter rule {{ seq.icmp_request }} action 'accept'
set firewall ipv4 input filter rule {{ seq.icmp_request }} icmp type-name 'echo-request'
set firewall ipv4 input filter rule {{ seq.icmp_request }} protocol 'icmp'

set firewall ipv4 input filter rule {{ seq.icmp_fragmentation_needed }} description 'Allow ICMP fragmentation needed to prevent PMTUD blackhole'
set firewall ipv4 input filter rule {{ seq.icmp_fragmentation_needed }} action 'accept'
set firewall ipv4 input filter rule {{ seq.icmp_fragmentation_needed }} icmp type '3'
set firewall ipv4 input filter rule {{ seq.icmp_fragmentation_needed }} icmp code '4'

set firewall ipv4 input filter rule {{ seq.ssh_limit_drop }} description 'SSH limits'
set firewall ipv4 input filter rule {{ seq.ssh_limit_drop }} action 'drop'
set firewall ipv4 input filter rule {{ seq.ssh_limit_drop }} destination port '{{ firewall.v4.ssh.port }}'
set firewall ipv4 input filter rule {{ seq.ssh_limit_drop }} protocol 'tcp'
set firewall ipv4 input filter rule {{ seq.ssh_limit_drop }} recent count '3'
set firewall ipv4 input filter rule {{ seq.ssh_limit_drop }} recent time minute
set firewall ipv4 input filter rule {{ seq.ssh_limit_drop }} state new 'enable'

set firewall ipv4 input filter rule {{ seq.ssh }} description 'Allow SSH from trusted networks'
set firewall ipv4 input filter rule {{ seq.ssh }} action 'accept'
set firewall ipv4 input filter rule {{ seq.ssh }} source group network-group '{{ firewall.v4.ssh.network_group }}'
set firewall ipv4 input filter rule {{ seq.ssh }} protocol 'tcp'
set firewall ipv4 input filter rule {{ seq.ssh }} destination port '{{ firewall.v4.ssh.port }}'

set firewall ipv4 input filter rule {{ seq.bogons }} description 'Drop bogons networks'
set firewall ipv4 input filter rule {{ seq.bogons }} action 'drop'
set firewall ipv4 input filter rule {{ seq.bogons }} source group network-group '{{ firewall.v4.bogon.network_group }}'

set firewall ipv4 input filter rule 10000 description 'Drop everything else'
set firewall ipv4 input filter rule 10000 action 'drop'
""")

# Template for output rules
output_v4_rules = Template("""
# Output rules
set firewall ipv4 output filter default-action 'accept'
""")


# def generate_firewall_rules(config: dict, template) -> str:
#     """Generate firewall rules"""
#     return template.render(config)

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

    print(generate_firewall_rules(config, network_group_v4))
    print(generate_firewall_rules(config, local_v4_rules))
    print(generate_firewall_rules(config, output_v4_rules))
