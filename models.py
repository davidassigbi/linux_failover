#!/usr/bin/env python3.9
from abc import ABC, abstractmethod
import abc
from dataclasses import dataclass
from icmplib import ping

@dataclass
class Provider:
    interface_name: str = "eth0"
    ipv4_address: str = "10.10.10.1"
    gateway: str = "10.10.10.254"
    network: str = "10.10.10.0/24"
    rt_table_name: str = "R1"
    rt_table_id: int = 1
    failed_checks_count: int = 0
    consecutive_failed_checks_count: int = 0
    consecutive_succeeded_checks: int = 0
    
    @property
    def id(self):
        return self.rt_table_name


@dataclass
class TestResult:
    result: bool = False


class TestScenario(abc.ABC):
    @abstractmethod
    def run_test(p: Provider) -> TestResult:
        raise NotImplementedError()
    

class ConnectionStateChangeHandler:
    def handle(p: Provider, status):
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


