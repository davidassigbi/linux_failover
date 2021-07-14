#!/usr/bin/env bash
source config.sh


function add_routing_for_primary_interface {
	ip route add ${NETWORK} dev ${PRIMARY_IF} src ${PRIMARY_IF_ADDR} table ${ISP1_TABLE}
	ip route add default via ${PRIMARY_GW} dev ${PRIMARY_IF} table ${ISP1_TABLE}
	ip rule add from ${PRIMARY_IF_ADDR} table ${ISP1_TABLE}
}

function add_routing_for_backup_interface {
	ip route add ${NETWORK} dev ${BACKUP_IF} src ${BACKUP_IF_ADDR} table ${ISP2_TABLE}
	ip route add default via ${BACKUP_GW} dev ${BACKUP_IF} table ${ISP2_TABLE}
	ip rule add from ${BACKUP_IF_ADDR} table ${ISP2_TABLE}
}

#ip route del default
#ip route add default scope global nexthop via ${BACKUP_GW} dev ${BACKUP_IF} nexthop via ${PRIMARY_GW} dev ${PRIMARY_IF}
#DELETE_DEFAULT_ROUTE
#ADD_DEFAULT_MAIN_BEING_PRIMARY_IF

delete_default_routes

add_routing_for_primary_interface
add_routing_for_backup_interface

switch_to_primary_interface
