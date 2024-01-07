#!/usr/bin/env bash

cp vyos-1.4.0-cloud-init-2G-qemu.qcow2 /var/lib/libvirt/images/vyos_kvm.qcow2

virt-install -n vyos_r1 \
   --ram 4096 \
   --vcpus 2 \
   --cloud-init meta-data=meta-data,user-data=user-data \
   --os-variant debian10 \
   --network network=default \
   --graphics vnc \
   --hvm \
   --virt-type kvm \
   --disk path=/var/lib/libvirt/images/vyos_kvm.qcow2,bus=virtio \
   --import \
   --noautoconsole
