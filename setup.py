#!/usr/bin/env python3
from subprocess import run
from config import *

def add_routing_table(network:str, interface_name: str, interface_address: str, gateway: str, table_name: str):
    cmd = f"""ip route add {network} dev {interface_name} src {interface_address} table {table_name}
    ip route add default via {gateway} dev {interface_name} table {table_name}
    ip rule add from {interface_address} table {table_name}"""
    run(cmd, **DEFAULT_SHELL_OPTIONS)


def add_routing_for_primary_interface():
    # subprocess.run(f"ip route add {NETWORK} dev {PRIMARY_IF} src {PRIMARY_IF_ADDR} table {ISP1_TABLE}", shell=True, text=True)
    # subprocess.run(f"ip route add default via {PRIMARY_GW} dev {PRIMARY_IF} table {ISP1_TABLE}", shell=True, text=True)
    # subprocess.run(f"ip rule add from {PRIMARY_IF_ADDR} table {ISP1_TABLE}", shell=True, text=True)
    add_routing_table(NETWORK, PRIMARY_IF, PRIMARY_IF_ADDR, PRIMARY_GW, ISP1_TABLE)


def add_routing_for_backup_interface():
    # subprocess.run(f"ip route add {NETWORK} dev {BACKUP_IF} src {BACKUP_IF_ADDR} table {ISP2_TABLE}", shell=True, text=True)
    # subprocess.run(f"ip route add default via {BACKUP_GW} dev {BACKUP_IF} table {ISP2_TABLE}", shell=True, text=True)
    # subprocess.run(f"ip rule add from {BACKUP_IF_ADDR} table {ISP2_TABLE}", shell=True, text=True)
    add_routing_table(NETWORK, BACKUP_IF, BACKUP_IF_ADDR, BACKUP_GW, ISP2_TABLE)

delete_default_routes()

add_routing_for_primary_interface()
add_routing_for_backup_interface()

switch_to_primary_interface()
