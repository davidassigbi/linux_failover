#!/usr/bin/env python3
from subprocess import DEVNULL, PIPE, run

CHECK_DELAY = 5
CHECK_IP = "1.1.1.1"

NETWORK = "10.10.1.0/24"

class Provider:
    interface_name = "eth0"
    interface_address = "10.10.1.1"
    gateway = "10.10.1.254"
    rt_table_name = "R1"
    rt_table_id = 1
    network = "10.10.1.0/24"
    def __init__(self, sth) -> None:
        self.sth = sth
    
PRIMARY_IF = "eth0"
PRIMARY_IF_ADDR = "10.10.1.1"
PRIMARY_GW = "10.10.1.254"
ISP1_TABLE = "R1"

BACKUP_IF = "eth1"
BACKUP_IF_ADDR = "10.10.1.2"
BACKUP_GW = "10.10.1.254"
ISP2_TABLE = "R2"

START_METRIC = 100

DEFAULT_SHELL_OPTIONS = { 
    "shell": True,
    "text": True,
    "close_fds": True,
    "timeout": 2
}
# def run(*args, **kwargs):
#     return run(*args, **kwargs, shell=True, text=True)

def current_main_interface() -> str:
    """Will return the default interface with the higher proority"""
    #{ ip route  | grep "metric 100" | sed -rn "s/^.*dev ([^ ]*).*$/\1/p"; }
    res = run('ip route | grep "metric 100" | sed -rn "s/^.*dev ([^ ]*).*$/\1/p"', **DEFAULT_SHELL_OPTIONS, capture_output=True)
    return res.stdout


def delete_default_routes() ->  None:
    """Will delete all the default routes"""
    # if $(ip route | grep -q default) ; then
    #     for i in `seq 1 $(ip route | grep -c default)`; do ip route del default ; done
    # fi
    
    default_routes_count = run("ip route | grep -c default", capture_output=True, **DEFAULT_SHELL_OPTIONS).stdout.strip()
    for _ in range(0, int(default_routes_count)):
        run("ip route del default", **DEFAULT_SHELL_OPTIONS)
    return


def add_default_route(interface_name: str, gateway_address: str, metric: int) -> None:
    run(f"ip route add default via {gateway_address} dev {interface_name} metric {metric}", **DEFAULT_SHELL_OPTIONS)

def switch_to_primary_interface() -> None:
    delete_default_routes()
    add_default_route(PRIMARY_IF, PRIMARY_GW, START_METRIC)
    add_default_route(BACKUP_IF, BACKUP_GW, ++START_METRIC)


def switch_to_backup_interface() -> None:
    delete_default_routes()
    add_default_route(BACKUP_IF, BACKUP_GW, START_METRIC)
    add_default_route(PRIMARY_IF, PRIMARY_GW, ++START_METRIC)


def switch_to_interface() -> None:
    return 


def main():
    # ndb = pyroute2.NDB()
    # print(ndb.routes['default'])
    # print(ndb.routes.dump())
    # print(ndb.addresses.summary())  # Print interfaces and associated IP
    # print(ndb.interfaces.summary())
    return


if __name__ == "__main__":
    main()
