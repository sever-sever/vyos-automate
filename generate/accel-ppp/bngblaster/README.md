
Test PPPoE-server with `bngblaster` https://rtbrick.github.io/bngblaster/quickstart.html

Example of PPPoE-server VyOS configuration:
```
set interfaces ethernet eth1 vif 23
set service pppoe-server access-concentrator 'ACN'
set service pppoe-server authentication local-users username foo password 'bar'
set service pppoe-server authentication mode 'local'
set service pppoe-server client-ip-pool name ONE gateway-address '100.64.0.1'
set service pppoe-server client-ip-pool name ONE subnet '100.64.0.0/18'
set service pppoe-server interface eth1
set service pppoe-server interface eth1.23
set service pppoe-server name-server '100.64.0.1'
set service pppoe-server name-server '203.0.113.1'
set service pppoe-server session-control 'disable'

```
NOTE: There is no option to enable "any login" yet, we have to change it in `/run/accel-pppd/pppoe.conf`
```
...
[auth]
any-login=1
...
```

restart `sudo systemctl restart accel-ppp@pppoe.service`

On the bngblaster node start test for 1000 session:
```
sudo bngblaster -C pppoe.json -I -c 1000
```

Example with RADIUS authentication:
```
set container name radius allow-host-networks
set container name radius description 'Radius'
set container name radius image 'dchidell/radius-web'
set container name radius volume clients destination '/etc/raddb/clients.conf'
set container name radius volume clients source '/config/containers/radius/clients'
set container name radius volume users destination '/etc/raddb/users'
set container name radius volume users source '/config/containers/radius/users'
set service pppoe-server access-concentrator 'ACN'
set service pppoe-server authentication mode 'radius'
set service pppoe-server authentication radius rate-limit attribute 'Cisco-AVPair'
set service pppoe-server authentication radius rate-limit enable
set service pppoe-server authentication radius rate-limit vendor 'Cisco'
set service pppoe-server authentication radius server 203.0.113.1 key 'vyos-secret'
set service pppoe-server client-ip-pool name ONE gateway-address '100.64.0.1'
set service pppoe-server client-ip-pool name ONE subnet '100.64.0.0/17'
set service pppoe-server gateway-address '100.64.0.1'
set service pppoe-server interface eth1 vlan '23-1000'
set service pppoe-server name-server '100.64.0.1'
set service pppoe-server name-server '203.0.113.1'
set service pppoe-server session-control 'disable'

```

Example of IPoE-server VyOS configuration:
```
set service ipoe-server authentication mode 'noauth'
set service ipoe-server client-ip-pool name first-pool gateway-address '100.64.0.1'
set service ipoe-server client-ip-pool name first-pool subnet '100.64.0.2/18'
set service ipoe-server interface eth1
set service ipoe-server interface eth1.23

```

On the bngblaster node start test for 1000 session (limit to 800 by default):
```
sudo bngblaster -C ipoe.json -I -c 1000
```

On the bngblaster node start test for 8000 session:
```
sudo bngblaster -C ipoe-vlans.json -I
```
