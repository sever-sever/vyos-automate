#!/usr/bin/env bash

#cp /tmp/vyos_raw_image.qcow2 /var/lib/libvirt/images/vyos_kvm.qcow2
cp vyos-1.4.0-cloud-init-2G-qemu.qcow2 /var/lib/libvirt/images/vyos_kvm.qcow2

virt-install -n vyos_r1 \
   --ram 2048 \
   --vcpus 2 \
   --cdrom seed.iso \
   --os-variant debian10 \
   --network network=default \
   --graphics vnc \
   --hvm \
   --virt-type kvm \
   --disk path=/var/lib/libvirt/images/vyos_kvm.qcow2,bus=virtio \
   --import \
   --noautoconsole

