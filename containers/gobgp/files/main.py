#!/usr/bin/env python3

import subprocess
import json
from concurrent.futures import ThreadPoolExecutor

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


def opcode_to_operator_map(opcode: int, output_format: str = 'op') -> str:
    """Maps BGP FlowSpec opcode to operator or nftables operator
    https://datatracker.ietf.org/doc/html/draft-ietf-idr-rfc5575bis-06#section-4.2.3
    """
    opcodes = {
        129: {'op': '==', 'nft': '=='},
        131: {'op': '>=', 'nft': '>='},
        139: {'op': '&&', 'nft': '&&'},
        145: {'op': '=', 'nft': '=='},
        146: {'op': '>', 'nft': '>'},
        148: {'op': '<', 'nft': '<'},
        149: {'op': '<=', 'nft': '<='},
    }
    return opcodes[opcode][output_format]


def parse_bgp_update(data):
    """Parse the BGP update message and generate nftables rules"""
    data = json.loads(data)
    action = 'accept'
    nft_cmd = ''
    for entry in data:
        print(entry)
        # Check if 'afi' and 'safi' are present in the attributes
        # Interested only afi 'IPv4 unicast', safi 'IPv4 flow-spec'
        afi = ''
        safi = ''
        for attr in entry.get('attrs', []):
            if 'afi' in attr and 'safi' in attr:
                afi = attr['afi']
                safi = attr['safi']
        if not (afi == 1 and safi == 133):
            continue

        nlri = entry.get('nlri', {}).get('value')
        for rule in nlri:
            rule_type = rule.get('type')
            match_filter = type_to_match_filter_map(rule_type)
            match_filter_nft = type_to_match_filter_map(rule_type, output_format='nft')

            # Packet length find op and value
            op_packet_length = ''
            if match_filter == 'packet_length':
                op_packet_length = opcode_to_operator_map(
                    rule.get('value')[0].get('op'), output_format='nft')
                print(f'{match_filter} op: {op_packet_length}')

            match_values = rule.get('value')
            if isinstance(match_values, dict):
                if 'prefix' in match_values:
                    prefix = match_values['prefix']
                    print(f'{match_filter}: {prefix}')
                    nft_cmd += f'{match_filter_nft} {prefix} '
            elif isinstance(match_values, list):
                print(match_filter, ':', match_values[0].get('value'))
                nft_cmd += f' {match_filter_nft} {op_packet_length} {match_values[0].get("value")}'

    print('-' * 20)
    print(f'nft add rule inet filter input {nft_cmd} counter {action}')


def process_bgp_update(json_data):
    parse_bgp_update(json_data)
    print('-' * 20, 'process_bgp_update')


if __name__ == '__main__':
    # Read and process the command output line by line
    # Adjust max_workers as needed
    with ThreadPoolExecutor(max_workers=5) as executor:
        for line in iter(process.stdout.readline, b''):
            print('DEBUG ORIGINAL data:', line)
            # Decode the JSON data
            json_data = line.decode("utf-8").strip()
            #print('DEBUG ORIGINAL data:', json_data)

            # Submit the task for processing
            executor.submit(process_bgp_update, json_data)

    # Wait for the command to finish
    process.wait()
