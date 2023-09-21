#!/usr/bin/env bash

# Usage: ./main.sh
# This script encodes the specified 'remote-commands.sh', sends it to a remote VyOS host,
# and executes the commands on the remote host.

# Remote VyOS host
remote_host="192.168.122.14"
remote_user="vyos"
remote_commands="remote-commands.sh"

# Ensure the script file exists
if [ ! -e "$remote_commands" ]; then
    echo "Error: Remote commands script '$remote_commands' not found."
    exit 1
fi

# Commands which we send to remote host in script
CMDS=$(base64 -w0 remote-commands.sh)

ssh ${remote_user}@${remote_host} "echo $CMDS | base64 -d | sudo bash"
