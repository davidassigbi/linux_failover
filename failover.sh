#!/usr/bin/env bash

# Set defaults if not provided by environment
CHECK_DELAY=${CHECK_DELAY:-5}
CHECK_IP=${CHECK_IP:-1.1.1.1}
PRIMARY_IF=${PRIMARY_IF:-eth0}
PRIMARY_IF_ADDR=${PRIMARY_IF_ADDR:-10.10.1.1}
PRIMARY_GW=${PRIMARY_GW:-10.10.1.254}
BACKUP_IF=${BACKUP_IF:-eth1}
BACKUP_IF_ADDR=${BACKUP_IF_ADDR:-10.10.1.2}
BACKUP_GW=${BACKUP_GW:-10.10.1.254}

DELETE_DEFAULT_ROUTE="ip route del default"
ADD_DEFAULT_MAIN_BEING_PRIMARY_IF="ip route add default scope global
nexthop via ${PRIMARY_GW} dev ${PRIMARY_IF} nexthop via ${BACKUP_GW} dev ${BACKUP_IF}"
ADD_DEFAULT_MAIN_BEING_BACKUP_IF="ip route add default scope global
nexthop via ${BACKUP_GW} dev ${BACKUP_IF} nexthop via ${PRIMARY_GW} dev ${PRIMARY_IF}"

# Compare arg with current default gateway interface for route to healthcheck IP
gateway_if() {
  # [[ "$1" = "$(ip r g "$CHECK_IP" | sed -rn 's/^.*dev ([^ ]*).*$/\1/p')" ]]
  [[ "$1" = "$(ip route  | grep next | head -1 | sed -rn 's/^.*dev ([^ ]*).*$/\1/p')" ]]
}

# Cycle healthcheck continuously with specified delay
while sleep "$CHECK_DELAY"
do
  # If healthcheck succeeds from primary interface
  if ping -I "$PRIMARY_IF_ADDR" -c1 "$CHECK_IP" &>/dev/null
  then
    # Are we using the backup?
    if gateway_if "$BACKUP_IF"
    then # Switch to primary
		echo "Switching to $PRIMARY_IF"
		$DELETE_DEFAULT_ROUTE
		$ADD_DEFAULT_MAIN_BEING_PRIMARY_IF
		# ip r d default via "$BACKUP_GW" dev "$BACKUP_IF"
		# ip r a default via "$PRIMARY_GW" dev "$PRIMARY_IF"
    fi
  else
    # Are we using the primary?
    if gateway_if "$PRIMARY_IF"
    then # Switch to backup
		echo "Switching to $BACKUP_IF"
		$DELETE_DEFAULT_ROUTE
		$ADD_DEFAULT_MAIN_BEING_BACKUP_IF

		# ip r d default via "$PRIMARY_GW" dev "$PRIMARY_IF"
		# ip r a default via "$BACKUP_GW" dev "$BACKUP_IF"
    # else # Switch to primary
    #   ip r d default via "$BACKUP_GW" dev "$BACKUP_IF"
    #   ip r a default via "$PRIMARY_GW" dev "$PRIMARY_IF"
    fi
  fi
done

