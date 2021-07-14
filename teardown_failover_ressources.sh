#!/usr/bin/env bash
#echo "$IFACE" >> /var/log/custom-netlog

for i in `seq 1 $(ip rule | grep -c 10.10.1.1)`; do ip rule del from 10.10.1.1 table ISP1 > /dev/null 2>&1 ; done
for i in `seq 1 $(ip rule | grep -c 10.10.1.2)`; do ip rule del from 10.10.1.2 table ISP2 > /dev/null 2>&1 ; done

