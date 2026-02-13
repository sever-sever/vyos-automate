#!/usr/bin/env bash

cp vyos-1.5-kvm-ci-amd64-ttyS.qcow2 vyos-r1.qcow2

genisoimage \
    -output seed.img \
    -volid cidata -rational-rock -joliet \
    user-data meta-data

qemu-system-x86_64 \
  -enable-kvm \
  -machine accel=kvm:tcg \
  -cpu host \
  -m 1024 \
  -nographic \
  -serial mon:stdio \
  -netdev user,id=net0 \
  -device virtio-net-pci,netdev=net0 \
  -drive file=vyos-r1.qcow2,if=virtio,format=qcow2 \
  -drive file=seed.img,if=virtio,media=cdrom
