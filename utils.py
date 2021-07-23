#!/usr/bin/env python3.9
from subprocess import run
from typing import Callable, Iterable, TypeVar
from config import *

def current_main_interface() -> str:
    """Will return the default interface with the higher proority"""
    cmd = f'ip route | grep "metric {START_METRIC}" | sed -rn "s/^.*dev ([^ ]*).*$/\\1/p"'
    res = run(cmd, capture_output=True, **DEFAULT_SHELL_OPTIONS)
    print(f"{cmd=} {res.stdout.strip()=}")
    return res.stdout.strip()


def delete_default_routes() -> None:
    """Will delete all the default routes"""

    default_routes_count = int(run("ip route | grep -c default",
                                   capture_output=True, **DEFAULT_SHELL_OPTIONS).stdout.strip())
    print(f"ip route | grep -c default = {default_routes_count}")
    for_each(range(0, default_routes_count), lambda _: run(
        "ip route del default", **DEFAULT_SHELL_OPTIONS))


def add_default_route(interface_name: str, gateway_address: str, ipv4_address: str, metric: int) -> None:
    cmd = f"ip route add default via {gateway_address} dev {interface_name} src {ipv4_address} metric {metric}"
    print(f"Running => '{cmd}'")
    run(cmd, **DEFAULT_SHELL_OPTIONS)


def set_main_interface(interface_name: str = "eth0") -> None:
    print(f"Setting {interface_name} as main interface")
    # Reorder list so that the first interface be the one which we desire to switch
    reordered_providers_list = sorted(
        providers, key=lambda p: p.interface_name == interface_name, reverse=True)
    current_metric = START_METRIC - 1
    for p in reordered_providers_list:
        current_metric += 1
        add_default_route(p.interface_name, p.gateway, p.ipv4_address, current_metric)
    return


T = TypeVar("T")
def for_each(iterable: Iterable[T], func: Callable[[T], any]):
    for i in iterable:
        func(i)


def is_provider_reliable(interface_name: str) -> bool:
    if len(result_set[interface_name]) > 0:
        return result_set[interface_name][-1]
    return False


def next_reliabale_provider() -> Provider:
    """Return the next provider to have a reliable internet access"""
    provider: Provider = providers[0]
    for p in providers:
        if is_provider_reliable(p.interface_name):
            provider = p
            break
    return provider


def add_routing_table(network: str, interface_name: str, interface_address: str, gateway: str, table_name: str):
    cmd = f"""
    ip route add {network} dev {interface_name} src {interface_address} table {table_name}
    ip route add default via {gateway} dev {interface_name} table {table_name}
    ip rule add from {interface_address} table {table_name}""".strip()
    run(cmd, **DEFAULT_SHELL_OPTIONS)
    
    
def switch_provider(provider: Provider):
    delete_default_routes()
    set_main_interface(provider.interface_name)
    

def sticky_provider_index() -> int:
    return int(open(STICKY_PROVIDER_FILENAME).readline().strip())


# def main():
#     # ndb = pyroute2.NDB()
#     # print(ndb.routes['default'])
#     # print(ndb.routes.dump())
#     # print(ndb.addresses.summary())  # Print interfaces and associated IP
#     # print(ndb.interfaces.summary())
#     pass
