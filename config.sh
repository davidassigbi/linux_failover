#!/usr/bin/env bash
CHECK_DELAY="5"
CHECK_IP="1.1.1.1"

NETWORK="10.10.1.0/24"

PRIMARY_IF="eth0"
PRIMARY_IF_ADDR="10.10.1.1"
PRIMARY_GW="10.10.1.254"
ISP1_TABLE="ISP1"

BACKUP_IF="eth1"
BACKUP_IF_ADDR="10.10.1.2"
BACKUP_GW="10.10.1.254"
ISP2_TABLE="ISP2"

DELETE_DEFAULT_ROUTE="ip route del default"
ADD_DEFAULT_MAIN_BEING_PRIMARY_IF="ip route add default scope global
nexthop via ${PRIMARY_GW} dev ${PRIMARY_IF} nexthop via ${BACKUP_GW} dev ${BACKUP_IF}"
ADD_DEFAULT_MAIN_BEING_BACKUP_IF="ip route add default scope global
nexthop via ${BACKUP_GW} dev ${BACKUP_IF} nexthop via ${PRIMARY_GW} dev ${PRIMARY_IF}"
