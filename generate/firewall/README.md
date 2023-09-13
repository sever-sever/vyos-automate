Usage
```
$./vyos_basic_firewall.py

set firewall group network-group bogons-v4 description 'Bogons Networks'
set firewall group network-group bogons-v4 network 0.0.0.0/8
set firewall group network-group bogons-v4 network 10.0.0.0/8
set firewall group network-group bogons-v4 network 100.64.0.0/10
...
# Input rules
set firewall ipv4 input filter default-action 'drop'

set firewall ipv4 input filter rule 10 description 'Allow established/related'
set firewall ipv4 input filter rule 10 action 'accept'
set firewall ipv4 input filter rule 10 state established 'enable'
set firewall ipv4 input filter rule 10 state related 'enable'
...

```
