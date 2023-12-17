#!/bin/sh

# Available env variables:
#
# ROUTER_ID=192.0.2.10
# SYSTEM_AS=65001
# PEER_ADDRESS=192.0.2.1
# PEER_AS=65001


# Perform environment variable substitution
envsubst < /opt/gobgp/template/bgp.conf.template > /opt/gobgp/bgp.conf

# Run gobgpd with the generated config
exec gobgpd --config-file=/opt/gobgp/bgp.conf
