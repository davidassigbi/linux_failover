#!/usr/bin/env python3.9
import config
import utils as u
from subprocess import run


def flush_alternate_routing_tables() -> None:
    """Delete routing tables previously created for configured providers"""
    def flush(table_name: str) -> None:
        run(f"ip route flush table {table_name}", **config.DEFAULT_SHELL_OPTIONS)

    u.for_each(config.providers, lambda p: flush(p.rt_table_name))


def delete_alternate_routing_rules() -> None:
    """Delete any routing rule associated with a provider's ip address"""
    def delete(address: str) -> None:
        run(f"for prefix in `ip rule ls | grep {address} | sed 's/:.*//'`; do ip rule del pref $prefix ; done",
            **config.DEFAULT_SHELL_OPTIONS)

    u.for_each(config.providers, lambda p: delete(p.ipv4_address))

def main():
    """Remove any configuration created during the setup phase"""
    flush_alternate_routing_tables()
    
    delete_alternate_routing_rules()


if __name__ == "__main__":
    main()
