#!/usr/bin/env bash

# Set defaults if not provided by environment
source config.sh

# Cycle healthcheck continuously with specified delay
while sleep "$CHECK_DELAY"
do
	echo "Current interface : `current_main_interface`"
	# If healthcheck succeeds from primary interface
	if ping -I "$PRIMARY_IF_ADDR" -c1 "$CHECK_IP" &>/dev/null; then
		echo "Ping OK on primary interface"
		# Are we using the backup?
		if [[ `current_main_interface` == "$BACKUP_IF" ]]; then
			# Switch to primary
			echo "Switching to primary: $PRIMARY_IF"
			delete_default_routes
			switch_to_primary_interface
		fi
	else
		echo "Ping NOT OK on primary interface"
		# Are we using the primary?
		if [[ `current_main_interface` == "$PRIMARY_IF" ]]; then
		# Switch to backup
			echo "Switching to backup: $BACKUP_IF"
			delete_default_routes
			switch_to_backup_interface
		fi
	fi
done
