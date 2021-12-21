#!/usr/bin/env python3.9
import os
from config import DEFAULT_SHELL_OPTIONS, providers
from subprocess import run

# First of all cleanup every config before installing
cmd = f"""mkdir -p /etc/failover
systemctl disable failover.service
systemctl stop failover.service
rm /etc/systemd/system/failover.service
systemctl daemon-reload
systemctl reset-failed
rm -rf /etc/failover/*
{os.getcwd()}/teardown.py"""
run(cmd,**DEFAULT_SHELL_OPTIONS)

# Copy files over and make them executables
cmd = f"""mkdir -p /etc/failover
cp {os.getcwd()}/*.py /etc/failover/
chmod +x /etc/failover/*"""
for c in cmd.splitlines():
	run(c,**DEFAULT_SHELL_OPTIONS)

# Check if stuff has already been added for the instalaltion, if not then add those entries
# This is most usefull because I had as you guessed it run this hundreds of time
for p in providers:
	cmd = f"""
if ! grep -q "{p.rt_table_id}	{p.rt_table_name}" "/etc/iproute2/rt_tables"; then
	echo "{p.rt_table_id}	{p.rt_table_name}" >> /etc/iproute2/rt_tables
fi"""
	run(cmd,**DEFAULT_SHELL_OPTIONS)

cmd = \
"""
cp failover.service /etc/systemd/system/
systemctl enable failover.service
systemctl daemon-reload
systemctl start failover.service"""
for c in cmd.splitlines():
	run(c, **DEFAULT_SHELL_OPTIONS)
 
run("systemctl is-enabled failover.service", shell=True)
run("journalctl -f -u failover.service", shell=True)
