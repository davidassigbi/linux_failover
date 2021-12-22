#!/usr/bin/env python3.9
from config import *
import utils as u 


def main():
    """Setup required configuration for failover to be functional"""
    print(f"Removing default routes")
    u.delete_default_routes()
    print(f"Adding provider routes")
    for p in providers:
        print(f"Adding provider '{p.interface_name}' routing table and routing rule")
        u.add_routing_table_and_rule(
            network=p.network,
            interface_name=p.interface_name,
            interface_address=p.ipv4_address,
            gateway=p.gateway,
            table_name=p.rt_table_name)
    u.set_main_provider(providers[0].id)


if __name__ == "__main__":
    main()
