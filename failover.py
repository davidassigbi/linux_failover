#!/usr/bin/env python3.9
import time

from config import CHECK_INTERVAL
from utils import *


def main():
    """Cycle continuously and perform failover tasks by checking for sticky provider, running checks, making sure base provider is used"""
    
    # Cycle healthcheck continuously with specified delay
    while True:
        time.sleep(CHECK_INTERVAL)
        
        # Retrieve the id of the provider in use
        current_provider_id = current_main_provider_id()
        
        # Check for sticky provider 
        try :
            provider_id = sticky_provider_id()

            # Make sure there is actually a provider inside the file by check the returned value length
            if len(provider_id) > 0:
                # Check if the current provider is not already the sticky one to avoid performing useless operations
                if provider_id != current_provider_id:
                    sticky_provider = get_provider_by_id(provider_id)
                    switch_to_provider(sticky_provider.id)
                    print(f"Forcing '{sticky_provider.id}' as main provider")

                # Skip the remaining code as we explicitly want to use this provider
                continue
        except Exception as e:
            # Exception might happen because the sticky provider file is not readable for eg
            print(f"{e=}")

        run_provider_reliability_checks()
            
        enforce_best_provider_use(current_provider_id)

if __name__ == "__main__":
    main()
