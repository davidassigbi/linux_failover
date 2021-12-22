# Multigateway soft and ~transparent failover

## What is it ?
This is a set of scripts and service to perform what I call a soft failover from a main gateway to another with the particularty that one can have all gateways have the "same" IP address. This is actually very usefull in case you can not change that gateway LAN IP address (maybe because the provider doesn't allow to do so).

## How does it work ?
It is actually quite simple and maybe not the best way to do it but for me it worked like a charm.
Basically you have a configuration file in which you define all your providers and tests that you want to run to check whether a provider is healthy(has internet access).
The scripts then assume that an interface/provider is healthy once a check is successfull through that interface.
The checks are run at a user defined period against every single provider present on your linux firewall/router and these two things happen:
- Once a check fails through the current main provider, the program will look for the next provider that is reliable. And once it finds one, it sets it as the new main provider to ensure continued connectivity.

- It continues pinging the main interface and ASA the ping gets succesfull it switches back to the primary interface 

The actual decision about which routes should the packets flow through is controlled by `linux route metrics`. Those allow to have multiple default routes and only packets that don't go to a specific interface will get handled by the metric decision made by the kernel.

This allows to actually still be able to manually go through other inerfaces no matter its metric.

By default the script use a ping probe as health check. Advantage of ping as health check ? Well, I think, this almost include all cases you may ever want:
- If the link physically goes down ? the ping won't be successfull
- If it is an OS issue for example, then the ping will still be not successful and you can do whatever you want

## Configuration
There is only one configuration file for the script: config.py.
And inside that file all parameters are self explanatory, seriously they are, but here are they once again:

- `CHECK_INTERVAL = 5` : A floating point number to define the interval(in seconds) between two health checks.

- `START_METRIC = 100` : An integer used as the start metric for routes managed by the script. This is usefull in case you want to override routes defined by the script. For example if you set this value to `100` and you manually define a default route with a metric of `50`, then your new route will handle all outgoing packets by prevailing over routes defined by this script.


- `MAX_STORED_TEST_RESULT_COUNT = 50` : The number of health check results you want to store (If you're not sure just leave it to the default).

- `MAX_FAILED_CHECKS = 50, MIN_CONSECUTIVE_SUCCEEDED_CHECKS = 1` : Two integer values that you are very welcomed to customize. These two decide how you deem a provider to be unreliable. Here is a piece of code to show you these are used `is_reliable = failed_count <= config.MAX_FAILED_CHECKS and success_count > config.MIN_CONSECUTIVE_SUCCEEDED_CHECKS`.

- `STICKY_PROVIDER_FILENAME = "sticky.provider"` : If for some reason you decide that no matter what happens you wanted to stick a provider you can put that provider id inside this file. By doing so the script will stop performing health check and just set your sticky provider as the main one 

- `providers: list[Provider] = [ Provider(id="isp1", interface_name="eth1", ipv4_address="10.10.1.1", network="10.10.1.0/24", gateway="10.10.1.254", rt_table_name="R1", rt_table_id=1) ]` : Here you can define inside the sqaure brackets, your providers, by following the given example.

- `test_cases: list[TestScenario] = [ TestScenarioPing("8.8.8.8") ]` : These are the health checks to perform against all your providers. If you defined custom checks you can use them here. By default only the Ping checks are provided


**If you want to customize the health checks, you can look into the file `models.py`.**

## Installation
Once you are happy with your configuration run `$ sudo install.py` which will do the following things:
- First, try to uninstall any previous version of the program
- Copy the program files to the destination folder (/etc/failover)
- Add entries in your /etc/iproute2/rt_tables to perform policy based routing later
- Make those python files executable
- Install the service and launch it right away


## Uninstallation
If you want to remove the program from your system, you can run `$ sudo /etc/failover/uninstall.py` and everything realted to it should be gone.

PS: It is a python script so you can go inside and customize it like removing steps you don't want. Although I don't really recommend altering the program too much, if you're sure about what you're doing then feel FREE to tweak it as much as you want ;).
