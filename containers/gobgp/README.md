# gobgp container in VyOS

Build container
```shell
sudo podman build --net host --tag gobgp:one -f ./Dockerfile
```

VyOS configuration:
```shell
set container name gobgp image 'localhost/gobgp:one'
set container name gobgp network NET01 address '10.0.0.2'
set container name gobgp volume gobgp destination '/opt/gobgp'
set container name gobgp volume gobgp source '/config/containers/gobgp'

set protocols bgp system-as '65001'
set protocols bgp address-family ipv4-unicast network 100.64.0.0/24
set protocols bgp neighbor 10.0.0.2 address-family ipv4-flowspec
set protocols bgp neighbor 10.0.0.2 address-family ipv4-unicast
set protocols bgp neighbor 10.0.0.2 remote-as '65001'

```