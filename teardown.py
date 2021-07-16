#!/usr/bin/env python3
from config import *
from subprocess import run

def flush_alternate_routing_tables() -> None:
    def flush(table_name: str) -> None:
        run(f"ip route flush table {table_name}", **DEFAULT_SHELL_OPTIONS)

    flush(ISP1_TABLE)
    flush(ISP2_TABLE)


def delete_alternate_routing_rules() -> None:
    def delete(address: str) -> None:
        run(f"for prefix in `ip rule ls | grep {address} | sed 's/:.*//'`; do ip rule del pref $prefix ; done", **DEFAULT_SHELL_OPTIONS)

    delete(PRIMARY_IF_ADDR)
    delete(BACKUP_IF_ADDR)

#ip rule del pref #rule-id
#ip rule ls | grep 169.254.0.0 | sed "s/:.*//" | xargs

flush_alternate_routing_tables()

delete_alternate_routing_rules()