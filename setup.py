#!/usr/bin/env python3.9
from config import providers
from utils import add_routing_table, delete_default_routes, set_main_interface


def main():
    print(f"Removing default routes")
    delete_default_routes()
    print(f"Adding provider routes")
    for p in providers:
        print(f"Adding provider '{p.interface_name}' routing table and routing rule")
        add_routing_table(
            network=p.network,
            interface_name=p.interface_name,
            interface_address=p.ipv4_address,
            gateway=p.gateway,
            table_name=p.rt_table_name)
    set_main_interface(providers[0])


if __name__ == "__main__":
    main()
