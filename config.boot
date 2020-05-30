firewall {
    all-ping enable
    broadcast-ping disable
    config-trap disable
    ipv6-receive-redirects disable
    ipv6-src-route disable
    ip-src-route disable
    log-martians enable
    name OUTSIDE-IN {
        default-action drop
        rule 10 {
            action accept
            state {
                established enable
                related enable
            }
        }
    }
    receive-redirects disable
    send-redirects enable
    source-validation disable
    syn-cookies enable
    twa-hazards-protection disable
}
interfaces {
    bonding bond0 {
        address 192.168.122.11/24
        description "Bond towards Packet"
        firewall {
            in {
                name OUTSIDE-IN
            }
        }
        hash-policy layer2
        mode 802.3ad
    }
    ethernet eth0 {
        bond-group bond0
        description "member of bond0"
        duplex auto
        smp-affinity auto
        speed auto
    }
    loopback lo {
    }
    vti vti1 {
        address 10.0.0.1/32
    }
}
nat {
    source {
        rule 100 {
            outbound-interface bond0
            source {
                address 10.20.0.0/24
            }
            translation {
                address masquerade
            }
        }
    }
}
policy {
    prefix-list TO-UPLINK {
        rule 10 {
            action permit
            prefix 100.100.0.0/24
        }
    }
    route-map UPLINK-OUT {
        rule 10 {
            action permit
            match {
                ip {
                    address {
                        prefix-list TO-UPLINK
                    }
                }
            }
        }
        rule 20 {
            action deny
        }
    }
}
protocols {
    bgp 65111 {
        address-family {
            ipv4-unicast {
                network 100.100.0.0/24 {
                }
            }
        }
        neighbor 10.0.0.2 {
            address-family {
                ipv4-unicast {
                    route-map {
                        export UPLINK-OUT
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as 65002
            timers {
                holdtime 30
                keepalive 10
            }
        }
        parameters {
            log-neighbor-changes
        }
        timers {
            holdtime 4
            keepalive 2
        }
    }
    static {
        route 0.0.0.0/0 {
            next-hop 192.168.122.1 {
            }
        }
    }
}
service {
    ssh {
        client-keepalive-interval 180
        port 22
    }
}
system {
    config-management {
        commit-revisions 100
    }
    console {
        device ttyS0 {
            speed 9600
        }
        device ttyS1 {
            speed 115200
        }
    }
    host-name new-hostname-r
    login {
        user vyos {
            authentication {
                encrypted-password $6$QxPS.uk6mfo$9QBSo8u1FkH16gMyAVhus6fU3LOzvLR9Z9.82m3tiHFAxTtIkhaZSWssSgzt4v4dGAL8rhVQxTg0oAG9/q11h/
                plaintext-password ""
            }
            level admin
        }
    }
    name-server 1.1.1.1
    name-server 8.8.8.8
    ntp {
        server 0.pool.ntp.org {
        }
        server 1.pool.ntp.org {
        }
        server 2.pool.ntp.org {
        }
    }
    syslog {
        global {
            facility all {
                level info
            }
            facility protocols {
                level debug
            }
        }
    }
    time-zone UTC
}


/* Warning: Do not remove the following line. */
/* === vyatta-config-version: "broadcast-relay@1:cluster@1:config-management@1:conntrack-sync@1:conntrack@1:dhcp-relay@2:dhcp-server@5:dns-forwarding@1:firewall@5:ipsec@5:l2tp@1:mdns@1:nat@4:ntp@1:pptp@1:qos@1:quagga@6:snmp@1:ssh@1:system@9:vrrp@2:wanloadbalance@3:webgui@1:webproxy@1:webproxy@2:zone-policy@1" === */
/* Release version: 1.2.5 */
