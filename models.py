#!/usr/bin/env python3.9
import collections
from dataclasses import dataclass
from enum import Enum
from typing import TypeVar
from icmplib import ping


T = TypeVar("T")
ProvidersTestResultMap = dict[str, collections.deque[bool]]


@dataclass
class Provider:
    interface_name: str = "eth0"
    ipv4_address: str = "10.10.10.1"
    gateway: str = "10.10.10.254"
    network: str = "10.10.10.0/24"
    rt_table_name: str = "R1"
    rt_table_id: int = 1
    
    @property
    def id(self):
        return self.interface_name


@dataclass
class TestResult:
    result: bool = False


class TestScenario():
    def run_test(p: Provider) -> TestResult:
        raise NotImplementedError()
    

@dataclass
class TestScenarioPing(TestScenario):
    target: str = None
    
    def run_test(self, provider: Provider) -> TestResult:
        host = ping(self.target, timeout=1, count=1,
                    privileged=True, source=provider.ipv4_address)
        return TestResult(result=host.is_alive)


@dataclass
class TestScenarioDig(TestScenario):
    target: str
    def run_test(p: Provider) -> TestResult:
        return super().run_test()
