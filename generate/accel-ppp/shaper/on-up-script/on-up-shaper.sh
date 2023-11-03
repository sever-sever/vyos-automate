#!/usr/bin/env bash
#
# Parse Cisco RADIUS attributes:
# Cisco-AVPair ip:sub-qos-policy-out=my-policy-10mbps-down
# Cisco-AVPair ip:sub-qos-policy-in=my-policy-10mbps-up
#
# Set speed based on the policy value (in mbps)
# The values of policy are defined in the policy.conf
# my-policy-10mbps-down 10
# my-policy-10mbps-up 10
# my-policy-20mbps-down 20
# my-policy-20mbps-up 20
#
# Change the path to the "policy.conf" file
#
# Viacheslav Hletenko 2023
#

CONFIG_POLICY_FILE="/config/scripts/accel-pppd/policy.conf"
RADATTR_FILE="/run/accel-pppd/radattr.${1}"


# Function to shape traffic based on the QoS policy
shape_traffic() {
    local interface=$1
    local qos_policy_out=$2
    local qos_policy_in=$3
    local rate_out
    local rate_in
    local burst

    # Read the rate based on the QoS policy for outbound traffic
    rate_out=$(grep "$qos_policy_out" "$CONFIG_POLICY_FILE" | grep -v '^#' | awk '{print $2}')

    # Read the rate based on the QoS policy for inbound traffic
    rate_in=$(grep "$qos_policy_in" "$CONFIG_POLICY_FILE" | grep -v '^#' | awk '{print $2}')

    rate_out=$(($rate_out * 1024 * 1024))
    rate_in=$(($rate_in * 1024 * 1024))
    burst=$(($rate_out / 20))

    tc qdisc del dev $interface ingress || true
    tc qdisc del dev $interface root || true

    # Outbound traffic
    tc qdisc add dev $interface root handle 1: htb r2q 10 default 1
    tc class add dev $interface parent 1: classid 1:1 htb rate ${rate_out}
    tc class add dev $interface parent 1:1 classid 1:1 htb rate ${rate_out} burst $burst quantum 1514 prio 20

    # Inbound traffic
    tc qdisc add dev $interface handle ffff: ingress
    tc filter add dev $interface parent ffff: protocol ip prio 50 u32 match ip src 0.0.0.0/0 police rate ${rate_in} burst $burst drop flowid :1

}


# Main script

# Check if interface argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <interface>"
    exit 1
fi

# Check if the radattr.pppX file exists
if [ ! -f "$RADATTR_FILE" ]; then
    echo "File $RADATTR_FILE not found."
    exit 1
fi


# Read the "sub-qos-policy-out" and "sub-qos-policy-in" values from the attribute file
qos_policy_out=$(grep -i "Cisco-AVPair ip:sub-qos-policy-out" "$RADATTR_FILE" | cut -d'=' -f2 | tr -d '[:space:]')
qos_policy_in=$(grep -i "Cisco-AVPair ip:sub-qos-policy-in" "$RADATTR_FILE" | cut -d'=' -f2 | tr -d '[:space:]')

# Shape traffic based on the QoS policies
shape_traffic "$1" "$qos_policy_out" "$qos_policy_in"

