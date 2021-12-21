#!/usr/bin/env python3.9
from subprocess import run
from typing import Callable, Iterable
from models import Provider, ProvidersTestResultMap, T
import config


def for_each(iterable: Iterable[T], func: Callable[[T], any]):
    for i in iterable:
        func(i)


def get_provider_by_id(id: str) -> Provider:
    matches = list(filter(lambda p: p.id == id, config.providers))
    if len(matches) > 0:
        return matches[0]
    raise LookupError(f"Unable to find a provider with: id {id}")


def current_main_provider_id() -> str:
    """Retrieve the provider currently having the highest priority/lowest metric"""

    cmd = f'ip route | grep "metric {config.START_METRIC}" | sed -rn "s/^.*dev ([^ ]*) src ([^ ]*).*$/\\1 \\2/p"'
    matching_providers: list[Provider]

    # Run command and extract interface name and ip address 
    res = run(cmd, capture_output=True, **config.DEFAULT_SHELL_OPTIONS)
    [interface_name, ipv4_address, *_] = res.stdout.strip().split(" ")
    
    # Use interface name and ip address to find provider
    matching_providers = list(filter(lambda p: p.interface_name ==
                              interface_name and p.ipv4_address == ipv4_address, config.providers))
    # print(f"{cmd=} {matching_providers=}")

    # Make sure a single provider matched with the interface name and ip address
    return matching_providers[0].id if len(matching_providers) == 1 else config.providers[0].id


def delete_default_routes() -> None:
    """Delete all the default routes on the system"""
    cmd = "ip route | grep -c default"

    # Retrieve default routes count from shell and convert it to python integer
    default_routes_count = int(
        run(
            cmd,
            capture_output=True,
            **config.DEFAULT_SHELL_OPTIONS
        ).stdout.strip()
    )
    # print(f"{cmd} = {default_routes_count}")

    # Actually loop and delete all the default routes
    for_each(range(0, default_routes_count), lambda _: run(
        "ip route del default", **config.DEFAULT_SHELL_OPTIONS))


def add_default_route(interface_name: str, gateway_address: str, ipv4_address: str, metric: int):
    """Add a default route to the main routing table based on function parameters"""
    cmd = f"ip route add default via {gateway_address} dev {interface_name} src {ipv4_address} metric {metric}"
    # print(f"{cmd=}")
    run(cmd, **config.DEFAULT_SHELL_OPTIONS)


def set_main_provider(provider_id: str = "eth1"):
    """Sets the provider with the id passed to be the one which route has the highest priority (lowest metric)"""

    print(f"Setting '{provider_id}' as main provider.")
    
    # Reorder providers list so that the first element is the provider with the id received as argument
    reordered_providers_list = sorted(
        config.providers, key=lambda p: p.id == provider_id, reverse=True)

    # Decrease the start metric so as to increase it as we loop through the providers and 
    # increase it back again to give providers down the list lower priority thus a higher metric
    current_metric = config.START_METRIC - 1
    for p in reordered_providers_list:
        # As we go near list end, priority decreases, remenber, the higher the number, the lower the priority
        current_metric += 1
        add_default_route(p.interface_name, p.gateway, p.ipv4_address, current_metric)


def last_failed_checks_count(provider_id: str, result_set: ProvidersTestResultMap = config.result_set):
    """Retrieve the total number of failed checks amongst those stored"""
    results = result_set[provider_id]
    count = 0

    # Reverse the list to loop backwards through it, as new values are appended and not prepended to the list
    for r in reversed(results):
        # Increase count on every False encoutered
        if r is False:
            count += 1
    return count


def last_consecutive_value_count(provider_id: str, value: bool = True, result_set: ProvidersTestResultMap = config.result_set):
    """Retrieve the successive count for a value inside this provider's check result array"""
    results = result_set[provider_id]
    count = 0
    # Reverse the list to loop backwards through it, as new values are appended and not prepended to the list
    for r in reversed(results):
        if r is not value:
            break
        count += 1
    return count


def last_consecutive_succeeded_checks_count(provider_id: str, result_set: ProvidersTestResultMap = config.result_set):
    return last_consecutive_value_count(provider_id, True)


def last_consecutive_failed_checks_count(provider_id: str, result_set: ProvidersTestResultMap = config.result_set):
    return last_consecutive_value_count(provider_id, False)


def is_provider_reliable(provider_id: str) ->  bool:
    """Check if a provider is reliable based on previous check results.
        The implemented alogirthm is like this:
        if there is at lease a check result available and 
        number of failed checks is below or equal the configured minimum of failed checks and
        number of recent successive succeeded checks is greater than the configured minimum if consecutive succeeded checks 
        then the provider is considered reliable
    """
    has_results: bool = len(config.result_set[provider_id]) > 0
    failed_count: int = last_failed_checks_count(provider_id)
    success_count: int = last_consecutive_succeeded_checks_count(provider_id)
    print(f"{provider_id=} {failed_count=}, {success_count=}")

    return has_results and \
    failed_count <= config.MAX_FAILED_CHECKS and \
    success_count > config.MIN_CONSECUTIVE_SUCCEEDED_CHECKS


def next_reliabale_provider() -> Provider:
    """Return the first reliable from the list of configured providers. Note: Order does matter a lot inside a list"""
    # Loop through the provider and once one is reliable return it and exit the function
    for p in config.providers:
        if is_provider_reliable(p.id):
            return p

    first_provider = config.providers[0]
    print(f"No reliable provider found: using first provider ({first_provider.id}).")
    # If no provider is found to be reliable return the first one
    return first_provider


def add_routing_table_and_rule(network: str, interface_name: str, interface_address: str, gateway: str, table_name: str):
    """Insert routing table and routing rule for a provider"""

    cmd = f"""
    ip route add {network} dev {interface_name} src {interface_address} table {table_name}
    ip route add default via {gateway} dev {interface_name} table {table_name}
    ip rule add from {interface_address} table {table_name}""".strip()
    run(cmd, **config.DEFAULT_SHELL_OPTIONS)


def switch_to_provider(provider_id: str):
    """Delete all default routes and then sets the provider as the main one"""
    delete_default_routes()
    set_main_provider(provider_id)


def sticky_provider_id() -> str:
    """Return the sticky provider id by reading it from the file"""
    return open(config.STICKY_PROVIDER_FILENAME).readline().strip()


def run_provider_reliability_checks():
    """Run reliabilty checks on all providers and store check results"""
    
    # Loop through providers list
    for p in config.providers:
        test_result: list[bool] = []
        # Loop through and run all test cases on current provider
        for test in config.test_cases:
            test_result.append(test.run_test(p).result)
        # Store True only if all checks succeeded
        config.result_set[p.id].append(all(test_result))


def enforce_best_provider_use(current_provider_id: str):
    """Make sure the first or most reliable provider is in use"""

    # Get the most reliable provider based on previous check results
    normal_current_provider = next_reliabale_provider()
    result_set = ""
    for k in config.result_set:
        result_set += f"{k}: {''.join(str(int(v)) for v in config.result_set[k])}\n"
    
    print(f"{result_set}")
    print(f"current_provider_id: {current_provider_id}")
    print(f"normal_current_provider_id: {normal_current_provider.id}")
    
    # If we're actually not using that provider then, switch on it
    if normal_current_provider.id != current_provider_id:
        switch_to_provider(normal_current_provider.id)
