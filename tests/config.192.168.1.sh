#!/usr/bin/env bash
CHECK_DELAY="5"
CHECK_IP="1.1.1.1"

NETWORK="192.168.1.0/24"

PRIMARY_IF="eth4"
PRIMARY_IF_ADDR="192.168.1.2"
PRIMARY_GW="192.168.1.254"
ISP1_TABLE="TGCOM"

BACKUP_IF="eth0"
BACKUP_IF_ADDR="192.168.1.1"
BACKUP_GW="192.168.1.254"
ISP2_TABLE="CANAL"

function delete_default_routes {
	if $(ip route | grep -q default) ; then
	    for i in `seq 1 $(ip route | grep -c default)`; do ip route del default ; done
	fi
}
function switch_to_primary_interface {
    route add default gw ${BACKUP_GW} dev ${BACKUP_IF}
    route add default gw ${PRIMARY_GW} dev ${PRIMARY_IF}
}
function switch_to_backup_interface {
    route add default gw ${PRIMARY_GW} dev ${PRIMARY_IF}
    route add default gw ${BACKUP_GW} dev ${BACKUP_IF}
}
