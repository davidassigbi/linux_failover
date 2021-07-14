#!/usr/bin/env bash

# Set defaults if not provided by environment
source config.sh

# Compare arg with current default gateway interface for route to healthcheck IP
gateway_if() {
  [[ "$1" = $(ip route  | grep next | head -1 | sed -rn "s/^.*dev ([^ ]*).*$/\1/p") ]]
}

# Cycle healthcheck continuously with specified delay
while sleep "$CHECK_DELAY"
do
	# If healthcheck succeeds from primary interface
	if ping -I "$PRIMARY_IF_ADDR" -c1 "$CHECK_IP" &>/dev/null
	then
		echo "Ping OK on primary interface"
		# Are we using the backup?
		if gateway_if "$BACKUP_IF"
		then # Switch to primary
			echo "Switching to primary: $PRIMARY_IF"
			$DELETE_DEFAULT_ROUTE
			$ADD_DEFAULT_MAIN_BEING_PRIMARY_IF
		fi
	else
		echo "Ping NOT OK on primary interface"
		# Are we using the primary?
		if gateway_if "$PRIMARY_IF"
		then # Switch to backup
			echo "Switching to backup: $BACKUP_IF"
			$DELETE_DEFAULT_ROUTE
			$ADD_DEFAULT_MAIN_BEING_BACKUP_IF
		fi
	fi
done
