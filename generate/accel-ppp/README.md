Example of PPPoE-server configuration
```
set service pppoe-server access-concentrator 'ACN'
set service pppoe-server authentication mode 'radius'
set service pppoe-server authentication radius server 203.0.113.1 key 'vyos-secret'
set service pppoe-server client-ip-pool start '100.64.222.10'
set service pppoe-server client-ip-pool stop '100.64.222.200'
set service pppoe-server extended-scripts on-up '/config/scripts/accel-pppd/on-up-shaper.sh'
set service pppoe-server gateway-address '100.64.222.1'
set service pppoe-server interface eth2
set service pppoe-server name-server '192.0.2.1'
```