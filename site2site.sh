#!/usr/bin/env bash

ESP_GRP="office-srv-esp"
IKE_GRP="office-srv-ike"
SECRET="SSSeeccRetT"
SOURCE_IP="203.0.113.1"
PEER_IP="203.0.113.2"
LOCAL_PREFIX="10.1.1.0/24"
REMOTE_PREFIX="192.168.1.0/24"
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
set vpn ipsec ipsec-interfaces interface $IPEC_IFACE
set vpn ipsec site-to-site peer $PEER_IP authentication mode 'pre-shared-secret'
set vpn ipsec site-to-site peer $PEER_IP authentication pre-shared-secret '$SECRET'
set vpn ipsec site-to-site peer $PEER_IP ike-group '$IKE_GRP'
set vpn ipsec site-to-site peer $PEER_IP local-address '198.51.100.3'
set vpn ipsec site-to-site peer $PEER_IP tunnel 0 allow-nat-networks 'disable'
set vpn ipsec site-to-site peer $PEER_IP tunnel 0 allow-public-networks 'disable'
set vpn ipsec site-to-site peer $PEER_IP tunnel 0 esp-group '$ESP_GRP'
set vpn ipsec site-to-site peer $PEER_IP tunnel 0 local prefix $LOCAL_PREFIX
set vpn ipsec site-to-site peer $PEER_IP tunnel 0 remote prefix $REMOTE_PREFIX

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
set vpn ipsec site-to-site peer $SOURCE_IP local-address '198.51.100.3'
set vpn ipsec site-to-site peer $SOURCE_IP tunnel 0 allow-nat-networks 'disable'
set vpn ipsec site-to-site peer $SOURCE_IP tunnel 0 allow-public-networks 'disable'
set vpn ipsec site-to-site peer $SOURCE_IP tunnel 0 esp-group '$ESP_GRP'
set vpn ipsec site-to-site peer $SOURCE_IP tunnel 0 local prefix $REMOTE_PREFIX
set vpn ipsec site-to-site peer $SOURCE_IP tunnel 0 remote prefix $LOCAL_PREFIX

"

# Config R1

# Config R2
