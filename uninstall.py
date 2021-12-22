#!/usr/bin/env python3.9
from config import DEFAULT_SHELL_OPTIONS
from subprocess import run

# First of all cleanup every config before installing
cmd = f"""mkdir -p /etc/failover
systemctl disable failover.service
systemctl stop failover.service
rm /etc/systemd/system/failover.service
systemctl daemon-reload
systemctl reset-failed
/etc/teardown.py
rm -rf /etc/failover/*
"""
run(cmd,
	**DEFAULT_SHELL_OPTIONS)
