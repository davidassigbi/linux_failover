#!/usr/bin/env bash
source config.sh

ip route add ${NETWORK} dev ${PRIMARY_IF} src ${PRIMARY_IF_ADDR} table ${ISP1_TABLE}
ip route add default via ${PRIMARY_GW} dev ${PRIMARY_IF} table ${ISP1_TABLE}
ip rule add from ${PRIMARY_IF_ADDR} table ${ISP1_TABLE}

ip route add ${NETWORK} dev ${BACKUP_IF} src ${BACKUP_IF_ADDR} table ${ISP2_TABLE}
ip route add default via ${BACKUP_GW} dev ${BACKUP_IF} table ${ISP2_TABLE}
ip rule add from ${BACKUP_IF_ADDR} table ${ISP2_TABLE}

ip route del default
ip route add default scope global nexthop via ${BACKUP_GW} dev ${BACKUP_IF} nexthop via ${PRIMARY_GW} dev ${PRIMARY_IF}
