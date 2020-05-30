#!/usr/bin/env bash

disk=$1
config_url="https://raw.githubusercontent.com/sever-sever/vyos-automate/master/config/config.boot"
run="/opt/vyatta/bin/vyatta-op-cmd-wrapper"

# Check that the disk arguments is set
if [ $# -ne 1 ]; then
    echo "Usage: $0 <disk>"
    # Show all disks in the system
    lsblk | grep disk | awk '{print $1}'
    exit 1
fi

# Download temp packages for autoinstall (1.2.x jessie)
curl --url http://ftp.de.debian.org/debian/pool/main/e/expect/expect_5.45-6_amd64.deb --output /tmp/expect.deb
curl --url http://ftp.de.debian.org/debian/pool/main/t/tcl8.6/libtcl8.6_8.6.2+dfsg-2_amd64.deb --output /tmp/libtcl8.deb
curl --url http://ftp.de.debian.org/debian/pool/main/e/expect/tcl-expect_5.45-6_amd64.deb --output /tmp/tcl-expect.deb

# Install temp packages
sudo dpkg -i /tmp/libtcl8.deb /tmp/tcl-expect.deb /tmp/expect.deb

# Load configuration from remote URL
curl --url $config_url --output /opt/vyatta/etc/config/config.boot

# Install VyOS with only one disk (detected) in the system.
install_one_disk() {
 expect <<EOF

    spawn $run install image

    expect "Would you like to continue?"  {send "Yes\r"}
    expect "Partition (Auto/Parted/Skip)"  {send "Auto\r"}
    expect "Install the image on? *d*"  {send "$disk\r"}
    expect "Continue?"  {send "Yes\r"}
    expect "How big of a root partition should I create?" {send "\r"}
    sleep 20
    expect "What would you like to name this image?" {send "\r"}
    expect "Which one should I copy to "  {send "/opt/vyatta/etc/config/config.boot\r"}
    expect "Enter password for user 'vyos':" {send "vyos\r"}
    expect "Retype password for user 'vyos':"  {send "vyos\r"}
    expect "Which drive should GRUB modify the boot partition on?" {send "$disk\r"}
    expect "vyos@vyos:~$" {send "\r"}

EOF
}

# Install VyOS on system which detect more then one disk. Without RAID.
# Installation will be only to one disk. Different prompts for one and 2 disks.
install_couple_disk() {
 expect <<EOF

    spawn $run install image

    expect "Would you like to continue?"  {send "Yes\r"}
    expect "Would you like to configure RAID"  {send "No\r"}
    expect "Partition (Auto/Parted/Skip)"  {send "Auto\r"}
    expect "Install the image on? *d*"  {send "$disk\r"}
    expect "Continue?"  {send "Yes\r"}
    expect "How big of a root partition should I create?" {send "\r"}
    sleep 20
    expect "What would you like to name this image?" {send "\r"}
    expect "Which one should I copy to "  {send "/opt/vyatta/etc/config/config.boot\r"}
    expect "Enter password for user 'vyos':" {send "vyos\r"}
    expect "Retype password for user 'vyos':"  {send "vyos\r"}
    expect "Which drive should GRUB modify the boot partition on?" {send "$disk\r"}
    expect "vyos@vyos:~$" {send "\r"}

EOF
}

# How many disks. Different interactive installers for one and more disks
if [ `lsblk | grep disk | awk '{print $1}' | wc -l` -eq 1 ]; then
    install_one_disk
else
    install_couple_disk
fi

