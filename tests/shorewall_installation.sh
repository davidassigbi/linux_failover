#!/usr/bin/env bash

cp /usr/share/doc/shorewall/examples/two-interfaces/{snat,stoppedrules,interfaces,policy,rules,zones} /etc/shorewall/

cp /usr/share/doc/shorewall/examples/two-interfaces/{snat,interfaces,policy,zones} /etc/shorewall/

cp /usr/share/shorewall/configfiles/{providers} /etc/shorewall/

cp /usr/share/shorewall/configfiles/{providers,hosts,tunnels} /etc/shorewall/

net     NET_IF          dhcp,tcpflags,nosmurfs,routefilter,logmartians,sourceroute=0,physical=eth0
loc     LOC_IF          tcpflags,nosmurfs,routefilter,logmartians,physical=eth1


snat
SNAT(10.10.10.1)		0.0.0.0/0       eth0
SNAT(10.10.10.2)		0.0.0.0/0       eth1
# MASQUERADE			10.10.3.0/24 	eth0
# MASQUERADE			10.10.3.0/24 	eth1

/etc/shorewall/providers
R1    1       1       -               eth0            10.10.10.254  track,balance    -
R2    2       2       -               eth1            10.10.10.254	track,balance    -


zones
fw      firewall
net0    ipv4
net1    ipv4
lan     ipv4

/etc/shorewall/interfaces
#ZONE INTERFACE OPTIONS
net0    eth0    tcpflags,nosmurfs,routefilter=0,arp_ignore=1,proxyarp=0,logmartians,sourceroute=0,physical=eth0
net1    eth1    tcpflags,nosmurfs,routefilter=0,arp_ignore=1,proxyarp=0,logmartians,sourceroute=0,physical=eth1
lan     eth2    tcpflags,ignore=1,nosmurfs,routefilter,logmartians,physical=eth2

/etc/shorewall/snat
# Remarquez qu’ici on fait le NAT vers les deux interfaces réseaux connectées aux routeurs
SNAT(10.10.1.1)   0.0.0.0/0       eth0
SNAT(10.10.1.2)   0.0.0.0/0       eth1

# Si nous n’utilisons pas Shorewall une simple règle de masquerade comme la suivante suffit
# iptables -tnat -APOSTROUTING -s 10.10.3.0/24 -j MASQUERADE


/etc/shorewall/policy

net0    all     ACCEPT
net1    all     ACCEPT
lan     all     ACCEPT

all     net0    ACCEPT
all     net1    ACCEPT
all     lan     ACCEPT

all     $FW     ACCEPT
$FW     all     ACCEPT
# THE FOLOWING POLICY MUST BE LAST
all all   REJECT    $LOG_LEVEL

Pour tester que notre configuration de base est correcte, nous pouvons faire pointer notre gateway sur l’adresse IP unique des routeurs des FAI et accéder à internet.
# ip route add default via 10.10.1.254
# ping 8.8.8.8