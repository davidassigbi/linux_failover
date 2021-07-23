#!/usr/bin/env python3.9
import time
from config import *
from utils import *


def main():
    # Cycle healthcheck continuously with specified delay
    while True:
        time.sleep(CHECK_DELAY)
        current_interface = current_main_interface()
        
        # Check for sticky provider 
        try :
            provider_index = sticky_provider_index()
            if provider_index >= 0:
                if providers[provider_index].interface_name != current_interface:
                    print(f"Forcing {providers[provider_index]=} as main provider")
                    switch_provider(providers[provider_index])
                continue
        except Exception as e:
            print(f"{e=}")

        # Run provider tests
        for p in providers:
            test_result: list[bool] = []
            for test in test_cases:
                test_result.append(test.run_test(p).result)
            result_set[p.interface_name].append(all(test_result))
            
        
        # Get the interface that base on previous result we should be on
        normal_current_provider = next_reliabale_provider()
        print(f"{result_set=}, {current_interface=}, {normal_current_provider=}")
        # If we're actually not on that interface then euuuuuh, switch on it
        if normal_current_provider.interface_name != current_interface:
            switch_provider(normal_current_provider)

if __name__ == "__main__":
    main()
