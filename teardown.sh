#!/usr/bin/env bash
source config.sh

ip route flush table ${ISP1_TABLE}
ip route flush table ${ISP2_TABLE}
for i in `seq 1 $(ip rule | grep -c ${PRIMARY_IF_ADDR})`; do ip rule del from ${PRIMARY_IF_ADDR} table ${ISP1_TABLE} > /dev/null 2>&1 ; done
for i in `seq 1 $(ip rule | grep -c ${BACKUP_IF_ADDR})`; do ip rule del from ${BACKUP_IF_ADDR} table ${ISP2_TABLE} > /dev/null 2>&1 ; done
