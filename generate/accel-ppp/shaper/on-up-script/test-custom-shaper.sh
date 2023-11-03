#!/usr/bin/env bash

# Viacheslav Hletenko 2023
#


# Define the network interface
INTERFACE="eth1"

rate_base="80"
rate_out="10"
rate_in="10"

rate_out_spec_prefixes=$rate_base
rate_in_spec_prefixes=$rate_base

rate_base=$(($rate_base * 1024 * 1024))
rate_out=$(($rate_out * 1024 * 1024))
rate_out_spec_prefixes=$(($rate_out_spec_prefixes * 1024 * 1024))
rate_in=$(($rate_in * 1024 * 1024))
rate_in_spec_prefixes=$(($rate_in_spec_prefixes * 1024 * 1024))


# Check if the network interface exists
if ! ip link show dev $INTERFACE > /dev/null 2>&1; then
    echo "Network interface $INTERFACE does not exist."
    exit 1
fi

# Delete existing qdisc to avoid conflicts
tc qdisc del dev $INTERFACE root 2>/dev/null || true
tc qdisc del dev $INTERFACE ingress 2>/dev/null || true

# Delete the ifb interface if it exists
ip link delete ifb-$INTERFACE 2>/dev/null || true
tc qdisc del dev ifb-$INTERFACE ingress 2>/dev/null || true

# Create the ifb interface
ip link add name ifb-$INTERFACE type ifb
ip link set dev ifb-$INTERFACE up


### OUT traffic
tc qdisc add dev $INTERFACE root handle 1: htb r2q 30 default b

tc class add dev $INTERFACE parent 1: classid 1:1 htb rate $rate_base
tc class add dev $INTERFACE parent 1:1 classid 1:a htb rate $rate_out_spec_prefixes ceil $rate_base burst 15k
tc class add dev $INTERFACE parent 1:1 classid 1:b htb rate $rate_out ceil $rate_in burst 15k

tc filter add dev $INTERFACE protocol ip parent 1: prio 1 u32 match ip dst 203.0.113.0/24 flowid 1:a

### IN traffic

# Redirect interface to ifb-x. As inbount traffic couldn't use filters
tc qdisc add dev $INTERFACE handle ffff: ingress
tc filter add dev $INTERFACE parent ffff: protocol ip u32 match u32 0 0 action mirred egress redirect dev ifb-$INTERFACE

# shape
tc qdisc add dev ifb-$INTERFACE root handle 1: htb r2q 30 default b
tc class add dev ifb-$INTERFACE parent 1: classid 1:1 htb rate $rate_base
tc class add dev ifb-$INTERFACE parent 1:1 classid 1:a htb rate $rate_in_spec_prefixes ceil $rate_base burst 15k
tc class add dev ifb-$INTERFACE parent 1:1 classid 1:b htb rate $rate_in ceil $rate_in burst 15k

tc filter add dev ifb-$INTERFACE protocol ip parent 1: prio 1 u32 match ip src 203.0.113.0/24 flowid 1:a


# tc -s class show dev eth1
# tc -d qdisc show dev eth1
# tc -p class show dev eth1
# tc -p filter show dev eth1
