#!/usr/bin/env bash

# Generate site2site ike1 configuration for local and remote peer
#

ESP_GRP="grp-ESP"
IKE_GRP="grp-IKE"
SECRET="SSSeeccRetT"
SOURCE_IP="100.64.0.1"
PEER_IP="100.64.0.2"
LEFT_PREFIX="10.111.111.0/24"
RIGHT_PREFIX="10.222.222.0/24"
IPSEC_IFACE="eth0"

echo
echo "### R1 local configuration

set vpn ipsec esp-group $ESP_GRP compression 'disable'
set vpn ipsec esp-group $ESP_GRP lifetime '1800'
set vpn ipsec esp-group $ESP_GRP mode 'tunnel'
set vpn ipsec esp-group $ESP_GRP pfs 'enable'
set vpn ipsec esp-group $ESP_GRP proposal 1 encryption 'aes256'
set vpn ipsec esp-group $ESP_GRP proposal 1 hash 'sha1'
set vpn ipsec ike-group $IKE_GRP ikev2-reauth 'no'
set vpn ipsec ike-group $IKE_GRP key-exchange 'ikev1'
set vpn ipsec ike-group $IKE_GRP lifetime '3600'
set vpn ipsec ike-group $IKE_GRP proposal 1 encryption 'aes256'
set vpn ipsec ike-group $IKE_GRP proposal 1 hash 'sha1'
set vpn ipsec ipsec-interfaces interface $IPSEC_IFACE
set vpn ipsec site-to-site peer $PEER_IP authentication mode 'pre-shared-secret'
set vpn ipsec site-to-site peer $PEER_IP authentication pre-shared-secret '$SECRET'
set vpn ipsec site-to-site peer $PEER_IP ike-group '$IKE_GRP'
set vpn ipsec site-to-site peer $PEER_IP local-address $SOURCE_IP
set vpn ipsec site-to-site peer $PEER_IP tunnel 0 allow-nat-networks 'disable'
set vpn ipsec site-to-site peer $PEER_IP tunnel 0 allow-public-networks 'disable'
set vpn ipsec site-to-site peer $PEER_IP tunnel 0 esp-group '$ESP_GRP'
set vpn ipsec site-to-site peer $PEER_IP tunnel 0 local prefix $LEFT_PREFIX
set vpn ipsec site-to-site peer $PEER_IP tunnel 0 remote prefix $RIGHT_PREFIX

### R1 if using NAT
set nat source rule 10 destination address $RIGHT_PREFIX
set nat source rule 10 'exclude'
set nat source rule 10 outbound-interface $IPSEC_IFACE
set nat source rule 10 source address $LEFT_PREFIX

### R2 remote configuration

set vpn ipsec esp-group $ESP_GRP compression 'disable'
set vpn ipsec esp-group $ESP_GRP lifetime '1800'
set vpn ipsec esp-group $ESP_GRP mode 'tunnel'
set vpn ipsec esp-group $ESP_GRP pfs 'enable'
set vpn ipsec esp-group $ESP_GRP proposal 1 encryption 'aes256'
set vpn ipsec esp-group $ESP_GRP proposal 1 hash 'sha1'
set vpn ipsec ike-group $IKE_GRP ikev2-reauth 'no'
set vpn ipsec ike-group $IKE_GRP key-exchange 'ikev1'
set vpn ipsec ike-group $IKE_GRP lifetime '3600'
set vpn ipsec ike-group $IKE_GRP proposal 1 encryption 'aes256'
set vpn ipsec ike-group $IKE_GRP proposal 1 hash 'sha1'
set vpn ipsec ipsec-interfaces interface $IPSEC_IFACE
set vpn ipsec site-to-site peer $SOURCE_IP authentication mode 'pre-shared-secret'
set vpn ipsec site-to-site peer $SOURCE_IP authentication pre-shared-secret '$SECRET'
set vpn ipsec site-to-site peer $SOURCE_IP ike-group '$IKE_GRP'
set vpn ipsec site-to-site peer $SOURCE_IP local-address $PEER_IP
set vpn ipsec site-to-site peer $SOURCE_IP tunnel 0 allow-nat-networks 'disable'
set vpn ipsec site-to-site peer $SOURCE_IP tunnel 0 allow-public-networks 'disable'
set vpn ipsec site-to-site peer $SOURCE_IP tunnel 0 esp-group '$ESP_GRP'
set vpn ipsec site-to-site peer $SOURCE_IP tunnel 0 local prefix $RIGHT_PREFIX
set vpn ipsec site-to-site peer $SOURCE_IP tunnel 0 remote prefix $LEFT_PREFIX

### R2 is using NAT
set nat source rule 10 destination address $LEFT_PREFIX
set nat source rule 10 'exclude'
set nat source rule 10 outbound-interface $IPSEC_IFACE
set nat source rule 10 source address $RIGHT_PREFIX

"
