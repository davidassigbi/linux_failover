#!/usr/bin/env python3
import os
from config import *
from subprocess import run

# First of all cleanup every config before installing

cmd = f"""mkdir -p /etc/id2real_failover &>/dev/null
systemctl disable failover.service &>/dev/null
systemctl stop failover.service &>/dev/null
rm /etc/systemd/system/failover.service &>/dev/null
systemctl daemon-reload &>/dev/null
systemctl reset-failed &>/dev/null
rm -rf /etc/id2real_failover/* &>/dev/null
{os.getcwd()}/teardown.py"""
run(cmd,**DEFAULT_SHELL_OPTIONS)

# Copy files over and make them executables
print(f"os.getcwd = {os.getcwd()}")
cmd = f"""mkdir -p /etc/id2real_failover
cp {os.getcwd()}/*.py /etc/id2real_failover/
chmod +x /etc/id2real_failover/*"""
for c in cmd.splitlines():
	run(c,**DEFAULT_SHELL_OPTIONS)

# Check if stuff has already been added for the instalaltion, if not then add those entries
# This is most usefull because I had as you guessed it run this hundreds of time
cmd = f"""
if ! grep -q "1	{ISP1_TABLE}" "/etc/iproute2/rt_tables"; then
	echo "1	{ISP1_TABLE}" >> /etc/iproute2/rt_tables
fi
if ! grep -q "2	{ISP2_TABLE}" "/etc/iproute2/rt_tables"; then
	echo "2	{ISP2_TABLE}" >> /etc/iproute2/rt_tables
fi"""
run(cmd,**DEFAULT_SHELL_OPTIONS)

cmd = """
cp failover.service /etc/systemd/system/
systemctl enable failover.service
systemctl daemon-reload
systemctl start failover.service"""
for c in cmd.splitlines():
	run(c,**DEFAULT_SHELL_OPTIONS)
 
run("systemctl status failover.service", shell=True)
