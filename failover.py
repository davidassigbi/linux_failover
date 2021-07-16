#!/usr/bin/env python3
import collections
from subprocess import run
import time
from typing import TypeVar
from config import *
import pythonping

class TestResult:
    result: bool = False
    def __init__(self, result: bool):
        self.result = result

def ping(target: str = "1.1.1.1") -> TestResult:
    response_list = pythonping.ping(target, verbose=False, timeout=1, count=1, df=True)
    return TestResult(response_list.success())

def _ping(interface: str = "1.1.1.1") -> TestResult:
    res = run(f"ping -c1 -I {interface} {CHECK_IP}", **DEFAULT_SHELL_OPTIONS)
    return TestResult(res.returncode == 0)

result_set = {
    PRIMARY_IF: collections.deque([], maxlen=50),
    BACKUP_IF: collections.deque([], maxlen=50)
}


def last(iterable: list):
    return iterable[-1]

# Cycle healthcheck continuously with specified delay
while True :
	time.sleep(CHECK_DELAY)
	result_set[PRIMARY_IF].append(ping(PRIMARY_IF_ADDR).result)
	result_set[BACKUP_IF].append(ping(BACKUP_IF_ADDR).result)
 	# If healthcheck succeeds from primary interface
	if last(result_set(PRIMARY_IF)) == True:
		print("Ping OK on primary interface")
		# Are we using the backup?
		if current_main_interface() == BACKUP_IF:
			# Switch to primary
			print(f"Switching to primary: {PRIMARY_IF}")
			delete_default_routes()
			switch_to_primary_interface()
	else:
		print("Ping NOT OK on primary interface")
		# Are we using the primary?
		if current_main_interface() == PRIMARY_IF and last(result_set[BACKUP_IF]) == True:
		# Switch to backup
			print(f"Switching to backup: {BACKUP_IF}")
			delete_default_routes()
			switch_to_backup_interface()
