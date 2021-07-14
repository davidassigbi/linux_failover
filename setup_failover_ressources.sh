#!/usr/bin/env bash
#echo "$IFACE" >> /var/log/custom-netlog

ip route add 10.10.1.0/24 dev eth0 src 10.10.1.1 table ISP1 > /dev/null 2>&1
ip route add default via 10.10.1.254 dev eth0 table ISP1 > /dev/null 2>&1
ip rule add from 10.10.1.1 table ISP1 > /dev/null 2>&1

#ip route del default > /dev/null 2>&1
#ip route add default scope global nexthop via 10.10.1.254 dev eth0 nexthop via 10.10.1.254 dev eth1 > /dev/null 2>&1

ip route add 10.10.1.0/24 dev eth1 src 10.10.1.2 table ISP2 > /dev/null 2>&1
ip route add default via 10.10.1.254 dev eth1 table ISP2 > /dev/null 2>&1
ip rule add from 10.10.1.2 table ISP2 > /dev/null 2>&1

ip route del default > /dev/null 2>&1
ip route add default scope global nexthop via 10.10.1.254 dev eth1 nexthop via 10.10.1.254 dev eth0 > /dev/null 2>&1

