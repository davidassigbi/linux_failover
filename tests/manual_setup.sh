if ! grep -qe "${ISP1_TABLE}" "/etc/iproute2/rt_tables"; then
	echo -e "1\t${ISP1_TABLE}" >> /etc/iproute2/rt_tables
fi
if ! grep -qe "${ISP2_TABLE}" "/etc/iproute2/rt_tables"; then
	echo -e "2\t${ISP2_TABLE}" >> /etc/iproute2/rt_tables
fi


source config.10.10.10.sh
ip route add ${NETWORK} dev ${PRIMARY_IF} src ${PRIMARY_IF_ADDR} table ${ISP1_TABLE}
ip route add default via ${PRIMARY_GW} dev ${PRIMARY_IF} table ${ISP1_TABLE}
ip rule add from ${PRIMARY_IF_ADDR} table ${ISP1_TABLE}
# ip rule add from ${PRIMARY_GW} to ${PRIMARY_IF_ADDR} table ${ISP1_TABLE}

ip route add ${NETWORK} dev ${BACKUP_IF} src ${BACKUP_IF_ADDR} table ${ISP2_TABLE}
ip route add default via ${BACKUP_GW} dev ${BACKUP_IF} table ${ISP2_TABLE}
ip rule add from ${BACKUP_IF_ADDR} table ${ISP2_TABLE}
# ip rule add from ${PRIMARY_GW} to ${BACKUP_IF_ADDR} table ${ISP2_TABLE}

ip route add default scope global \
nexthop via 10.10.10.254 dev eth0 weight 1 \
nexthop via 10.10.10.254 dev eth1 weight 1


ip route add default proto static scope global \
nexthop via 10.10.10.254 dev eth0 weight 1 \
nexthop via 10.10.10.254 dev eth1 weight 1

route add default gw 10.10.10.254 dev eth0
route add default gw 10.10.10.254 dev eth1

while true; do sleep 1 && ping -c 1 1.1.1.1 | grep time; done

ip route flush table ${ISP1_TABLE}
ip route flush table ${ISP2_TABLE}
for i in `seq 1 $(ip rule | grep -c ${PRIMARY_IF_ADDR})`; do ip rule del from ${PRIMARY_IF_ADDR} table ${ISP1_TABLE} > /dev/null 2>&1 ; done
for i in `seq 1 $(ip rule | grep -c ${BACKUP_IF_ADDR})`; do ip rule del from ${BACKUP_IF_ADDR} table ${ISP2_TABLE} > /dev/null 2>&1 ; done


iptables -t nat -D
-A POSTROUTING -s 172.16.16.0/24 -o eth0 -j SNAT --to-source 10.10.10.1
-A POSTROUTING -s 172.16.16.0/24 -o eth1 -j SNAT --to-source 10.10.10.2

iptables -t nat -A POSTROUTING -s 172.16.16.0/24 ! -o eth2 -j MASQUERADE


ip route add default via 10.10.10.254 dev eth0 metric 100
ip route add default via 10.10.10.254 dev eth1 metric 101

ip route add default via 10.10.10.254 dev eth0 metric 101
ip route add default via 10.10.10.254 dev eth1 metric 100

ip route del default
ip route del default


alias current_main_interface='ip route  | grep "metric 100" | sed -rn "s/^.*dev ([^ ]*).*$/\1/p"'


current_main_interface="ip route | grep \"metric 100\""

function current_main_interface { ip route  | grep "metric 100" | sed -rn "s/^.*dev ([^ ]*).*$/\1/p" }

