#!/usr/bin/env python3

import subprocess
import json

# Command to execute
command = "gobgp monitor global rib --json"

# Execute the command and capture its output
process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)


def type_to_match_filter_map(match_type: int, output_format: str = 'formatted') -> str:
    """Convert BGP attribute type to flowspec match traffic filter or nftables rule
    https://github.com/osrg/gobgp/blob/master/docs/sources/flowspec.md#match-traffic-filtering-rules
    """
    match_types = {
        1: {'formatted': 'destination_address', 'nft': 'ip daddr'},
        2: {'formatted': 'source_address', 'nft': 'ip saddr'},
        3: {'formatted': 'protocol', 'nft': 'ip protocol'},
        4: {'formatted': 'port', 'nft': 'tcp dport'},
        5: {'formatted': 'destination_port', 'nft': 'tcp dport'},
        6: {'formatted': 'source_port', 'nft': 'tcp sport'},
        7: {'formatted': 'icmp_type', 'nft': 'icmp type'},
        8: {'formatted': 'icmp_code', 'nft': 'icmp code'},
        9: {'formatted': 'tcp_flags', 'nft': 'tcp flags'},
        10: {'formatted': 'packet_length', 'nft': 'ip length'},
        11: {'formatted': 'dscp', 'nft': 'ip dscp'},
        12: {'formatted': 'fragment', 'nft': 'ip frag'},
        13: {'formatted': 'label', 'nft': 'ip label'},
        14: {'formatted': 'ether_type', 'nft': 'ether type'},
        15: {'formatted': 'source_mac', 'nft': 'ether saddr'},
        16: {'formatted': 'destination_mac', 'nft': 'ether daddr'},
        17: {'formatted': 'llc_dsap', 'nft': 'llc dsap'},
        18: {'formatted': 'llc_ssap', 'nft': 'llc ssap'},
        19: {'formatted': 'llc_control', 'nft': 'llc control'},
        20: {'formatted': 'snap', 'nft': 'snap'},
        21: {'formatted': 'vlan', 'nft': 'vlan'},
        22: {'formatted': 'cos', 'nft': 'ip dscp'},
        23: {'formatted': 'inner_vlan', 'nft': 'vlan'},
        24: {'formatted': 'inner_cos', 'nft': 'ip dscp'},
    }
    return match_types[match_type][output_format]


def parse_bgp_update(data):
    """Parse the BGP update message and generate nftables rules"""
    data = json.loads(data)
    action = 'accept'
    nft_cmd = ''
    for entry in data:
        print(entry)
        nlri = entry.get('nlri', {}).get('value')
        for rule in nlri:
            rule_type = rule.get('type')
            match_filter = type_to_match_filter_map(rule_type)
            match_filter_nft = type_to_match_filter_map(rule_type, output_format='nft')
            match_values = rule.get('value')
            if isinstance(match_values, dict):
                if 'prefix' in match_values:
                    print('-' * 20)
                    prefix = match_values['prefix']
                    print(f'{match_filter}: {prefix}')
                    nft_cmd += f'{match_filter_nft} {prefix} '
            elif isinstance(match_values, list):
                print(match_filter, ':', match_values[0].get('value'))
                nft_cmd += f' {match_filter_nft} {match_values[0].get("value")}'

    print('-' * 20)
    print(f'nft add rule inet filter input {nft_cmd} counter {action}')


# Read and process the command output line by line
for line in iter(process.stdout.readline, b''):
    # Decode the JSON data
    json_data = line.decode("utf-8").strip()

    # Process the data
    parse_bgp_update(json_data)
    print('-' * 20)

# Wait for the command to finish
process.wait()
