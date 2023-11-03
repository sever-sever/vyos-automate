
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
