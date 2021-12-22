#!/usr/bin/env python3.9
import collections
from models import *

CHECK_INTERVAL = 0.3
START_METRIC = 100
MAX_STORED_TEST_RESULT_COUNT = 50

MAX_FAILED_CHECKS = 50
MIN_CONSECUTIVE_SUCCEEDED_CHECKS = 1
STICKY_PROVIDER_FILENAME = "sticky.provider"

providers: list[Provider] = [
    Provider(id="isp1", interface_name="eth1", ipv4_address="10.10.1.1",
             network="10.10.1.0/24", gateway="10.10.1.254", rt_table_name="R1", rt_table_id=1),

    Provider(id="isp2", interface_name="eth2", ipv4_address="10.10.2.2",
             network="10.10.2.0/24", gateway="10.10.2.254", rt_table_name="R2", rt_table_id=2)
]

test_cases: list[TestScenario] = [
    TestScenarioPing("8.8.8.8"),
    TestScenarioPing("1.1.1.1")
]


# Internal variables
result_set: ProvidersTestResultMap = {
    p.id: collections.deque([], maxlen=MAX_STORED_TEST_RESULT_COUNT) for p in providers}

DEFAULT_SHELL_OPTIONS = {"shell": True,
                         "text": True, "close_fds": True, "timeout": 5}
