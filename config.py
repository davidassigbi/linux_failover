#!/usr/bin/env python3.9
import collections
from models import *

CHECK_DELAY = 5
START_METRIC = 100
DEFAULT_SHELL_OPTIONS = {"shell": True,
                         "text": True, "close_fds": True, "timeout": 5}

MAX_FAILED_CHECKS = 0
MAX_CONSCUTIVE_FAILED_CHECKS = 0
MIN_CONSCUTIVE_SUCCEEDED_CHECKS = 0
STICKY_PROVIDER_FILENAME = "sticky.provider"

providers: list[Provider] = [
    Provider(interface_name="eth0", ipv4_address="10.10.10.1",
             network="10.10.10.0/24", gateway="10.10.10.254", rt_table_name="R1", rt_table_id=1),
    Provider(interface_name="eth1", ipv4_address="10.10.10.2",
             network="10.10.10.0/24", gateway="10.10.10.254", rt_table_name="R2", rt_table_id=2)
]

result_set: dict[str, collections.deque[bool]] = {
    p.interface_name: collections.deque([], maxlen=50) for p in providers}

test_cases: list[TestScenario] = [
    TestScenarioPing("8.8.8.8"),
    TestScenarioPing("1.1.1.1")
]
