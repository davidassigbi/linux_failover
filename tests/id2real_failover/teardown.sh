#!/usr/bin/env bash
source config.sh

function flush_alternate_routing_tables {
	ip route flush table ${ISP1_TABLE}
	ip route flush table ${ISP2_TABLE}
}

function delete_alternate_routing_rules {
	for i in `seq 1 $(ip rule | grep -c ${PRIMARY_IF_ADDR})`; do ip rule del from ${PRIMARY_IF_ADDR} table ${ISP1_TABLE} ; done
	for i in `seq 1 $(ip rule | grep -c ${BACKUP_IF_ADDR})`; do ip rule del from ${BACKUP_IF_ADDR} table ${ISP2_TABLE} ; done
	# for i in `seq 1 $(ip rule | grep -c ${PRIMARY_IF_ADDR})`; do ip rule del from ${PRIMARY_IF_ADDR} table ${ISP1_TABLE} > /dev/null 2>&1 ; done
	# for i in `seq 1 $(ip rule | grep -c ${BACKUP_IF_ADDR})`; do ip rule del from ${BACKUP_IF_ADDR} table ${ISP2_TABLE} > /dev/null 2>&1 ; done
}

flush_alternate_routing_tables;
delete_alternate_routing_rules;
