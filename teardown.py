#!/usr/bin/env python3.9
from config import *
from utils import *
from subprocess import run


def flush_alternate_routing_tables() -> None:
    def flush(table_name: str) -> None:
        run(f"ip route flush table {table_name}", **DEFAULT_SHELL_OPTIONS)
    for_each(providers, lambda p: flush(p.rt_table_name))


def delete_alternate_routing_rules() -> None:
    def delete(address: str) -> None:
        run(f"for prefix in `ip rule ls | grep {address} | sed 's/:.*//'`; do ip rule del pref $prefix ; done",
            **DEFAULT_SHELL_OPTIONS)
    for_each(providers, lambda p: delete(p.ipv4_address))


def main():
    # ip rule del pref #rule-id
    # ip rule ls | grep 169.254.0.0 | sed "s/:.*//" | xargs
    flush_alternate_routing_tables()
    delete_alternate_routing_rules()


if __name__ == "__main__":
    main()
