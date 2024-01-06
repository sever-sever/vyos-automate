#!/usr/bin/env bash

rm -f seed.iso
genisoimage -output seed.iso -volid cidata -joliet -r user-data meta-data
