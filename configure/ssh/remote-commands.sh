
if [ $(id -gn) != vyattacfg ]; then
    exec sg vyattacfg "$0 $*"
fi

run="/opt/vyatta/bin/vyatta-op-cmd-wrapper"
source /opt/vyatta/etc/functions/script-template

uptime
$run show version
$run show interfaces

configure
set interfaces ethernet eth0 description 'WAN'
commit
exit

