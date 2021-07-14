# Two-Gateway soft and almost transparent failover

## What is it ?
This is actually a set of scripts and service to perform what i call a soft failover from a main gateway to another with the paticularty that one can have the two gateways have the same IP address. This is actually very usefull in case you can not change that gateway LAN IP address.

## How it works ?
It is actually quite simple and maybe not the best way to do it but for me it worked like a charm.
Basically the scripts assume that an interface is healthy once a ping to a user definied IP is successfull through that interface.
I then ping the IP address through the main interface periodically:
    - Once a ping fails, it switched back to the backup interface
    - It continues pinging the main interface and ASA the ping gets succesfull it switches back to the primary interface 

The actual decision about which routes should the packets flow through is controlled by `linux route metrics`. Those allow to have multiple default routes and only packets to don't go to a specific interface will get handled by the metric decision made by the kernel.

This allows to actually still be able to manually go through other inerfaces no matter its metric.

Advantage of ping as health check ? Well this almost include all cases you may ever want:
- If the link physically goes down ? the ping won't be successfull
- If it is an OS issue for example, then the ping will still be not successful and you can do whatever you want

## Configuration
There is only one configuration file for the script: config.sh.
And inside that file all parameters are self explanatory, seriously they are.

## Installation
Once you are happy with your configuration run the install.sh script which will do the following things:
- First of all content of the destination folder so as if it is a reinstall then everythging should be cleaned
- Deleting the service if it was present
- Copying the actual scripts over to the destination folder
- Adding entries in your /etc/iproute2/rt_tables to perform some policy based routing later
- Making those executable
- Installing the service and lanching it right away

PS: It is just a script so you can go inside and customize things like removing some steps you don't want.
