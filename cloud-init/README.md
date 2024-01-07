
# Docker
The Dockerfile has all required dependencies.
1. Download the `Dockerfile`
```
wget https://raw.githubusercontent.com/vyos/vyos-vm-images/current/Dockerfile
```
2. Build local image with name `vyos-vm-images` (only if you do not have it)
```
docker build --tag vyos-vm-images:latest -f ./Dockerfile .
```
3. Start and connect to the container:
```shell
docker run --rm -it --privileged -v $(pwd):/vm-build -v $(pwd)/images:/images -w /vm-build vyos-vm-images:latest bash
```
4. Clone repo
```
git clone https://github.com/vyos/vyos-vm-images.git && cd vyos-vm-images
```

# Generate qemu image
Generate qemu image based on local ISO
```shell
ansible-playbook qemu.yml -e disk_size=2 -e iso_local=./vyos-1.4.iso -e cloud_init=true -e cloud_init_ds=NoCloud -e grub_console=serial -e vyos_version=1.4.0 -e guest_agent=qemu -e enable_ssh=true
```

## Make seed ISO
```shell
mkisofs -joliet -rock -volid "cidata" -output seed.iso meta-data user-data
or
genisoimage -output seed.iso -volid cidata -joliet -r user-data meta-data
```
