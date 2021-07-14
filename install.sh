#!/usr/bin/env bash
source config.sh

# First of all cleanup every config before installing
systemctl disable failover.service
systemctl stop failover.service
rm /etc/systemd/system/failover.service
systemctl daemon-reload
systemctl reset-failed
rm -rf /etc/id2real_failover/*
./teardown.sh

# Copy files over and make them executables
mkdir -p /etc/id2real_failover
cp {config.sh,failover.sh,setup.sh,teardown.sh} /etc/id2real_failover/
chmod +x /etc/id2real_failover/*

# Check if stuff has already been added for the instalaltion, if not then add those entries
# This is most usefull because I had as you guessed it run this hundreds of time
if ! grep -q "1	${ISP1_TABLE}" "/etc/iproute2/rt_tables"; then
	echo "1	${ISP1_TABLE}" >> /etc/iproute2/rt_tables
fi
if ! grep -q "2	${ISP2_TABLE}" "/etc/iproute2/rt_tables"; then
	echo "2	${ISP2_TABLE}" >> /etc/iproute2/rt_tables
fi

cp failover.service /etc/systemd/system/
systemctl enable failover.service
systemctl daemon-reload
systemctl start failover.service
systemctl status failover.service
