#!/usr/bin/env bash
source config.sh
mkdir -p /etc/id2real_failover
cp {config.sh,failover.sh,setup.sh,teardown.sh} /etc/id2real_failover/
chmod +x /etc/id2real_failover/*
cp failover.service /etc/systemd/system/
#echo "1	${ISP1_TABLE}" >> /etc/iproute2/rt_tables
#echo "2	${ISP2_TABLE}" >> /etc/iproute2/rt_tables
#iptables -tnat -APOSTROUTING -s [PRIVATE_NETWORK/MASK] -j MASQUERADE
systemctl disable failover.service
systemctl stop failover.service
systemctl enable failover.service
systemctl start failover.service
systemctl status failover.service


