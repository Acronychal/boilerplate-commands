# Large enterprise topology with 2 remote sites connected via tunnel
- site one users admin
- site two servers


######### MAIN SITE ########


# Ubuntu Docker nodes

  - Edit and uncomment the following for DHCP using nano/vim /etc/network/interface

```
auto eth0
iface eth0 inet dhcp
	hostname C1-8

```
# R2

```
enable
configure terminal
hostname R2
ip domain-lookup
ip name-server 8.8.8.8
ip route 0.0.0.0 0.0.0.0 172.16.12.1
access-list 1 permit any
ip nat inside source list 1 interface g1 overload


interface loopback 0
ip address 1.1.3.1 255.255.255.255

interface g1
no shutdown
description "Uplink to ISP"
ip address 172.16.12.2 255.255.255.0
ip nat outside
exit

interface g2
no shutdown
ip nat inside
description "Link To DSW1"
ip address 10.111.110.1 255.255.255.0

interface g3
ip nat inside
no shutdown
description "Link To DSW2"
ip address 10.112.110.1 255.255.255.0


router ospf 1
network 1.1.3.1 0.0.0.0 area 0
network 10.111.110.0 0.0.0.255 area 0
network 10.112.110.0 0.0.0.255 area 0
default-information originate


end

interface tunnel 1
ip address 192.168.10.1 255.255.255.0
tunnel source 1.1.1.1
tunnel destination 2.2.2.1
exit

router eigrp 10
network 192.168.10.0
exit




```



# DSW1

```
enable
configure terminal
hostname DSW1
ip domain-lookup
ip name-server 8.8.8.8
ip routing


interface port-channel 10
description "PO 10 to DSW2"
no switchport
ip address 10.113.110.1 255.255.255.0
no shutdown

interface range g0/1-3
no switchport
channel-group 10 mode active
no shutdown

interface range g1/0-3
switchport
switchport trunk encapsulation dot1q
switchport mode trunk

vlan 100
vlan 200
vlan 300
vlan 400

interface vlan 100
description "STAFF"
ip address 10.110.10.254 255.255.255.0
standby 10 ip 10.110.10.1
no shutdown

interface vlan 200
description "HR"
ip address 10.110.20.254 255.255.255.0
standby 10 ip 10.110.20.1
no shutdown

interface vlan 300
description "GUESTS"
ip address 10.110.30.254 255.255.255.0
standby 10 ip 10.110.30.1
no shutdown

interface vlan 400
description "IT"
ip address 10.110.100.254 255.255.255.0
standby 10 ip 10.110.100.1
no shutdown

interface g0/0
description "Uplink to R2"
no switchport
ip address 10.111.110.2 255.255.255.0
no shutdown

interface loop 0
ip address 1.1.3.2 255.255.255.255

router ospf 1
network 1.1.3.2 0.0.0.0 area 0
network 10.111.110.0 0.0.0.0 area 0
network 10.110.10.0 0.0.0.255 area 0
network 10.110.20.0 0.0.0.255 area 0
network 10.110.30.0 0.0.0.255 area 0
network 10.110.100.0 0.0.0.255 area 0
passive-interface vlan 100
passive-interface vlan 200
passive-interface vlan 300
passive-interface vlan 400
default-information originate
exit





end


```

# DSW2

```

enable
configure terminal
hostname DSW2
ip domain-lookup
ip name-server 8.8.8.8
ip routing



interface port-channel 10
description "PO 10 to DSW1"
no switchport
ip address 10.113.110.2 255.255.255.0
no shutdown

interface range g0/1-3
no switchport
channel-group 10 mode active
no shutdown

interface range g1/0-3
switchport
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown

vlan 100
vlan 200
vlan 300
vlan 400

interface vlan 100
description "STAFF"
ip address 10.110.10.253 255.255.255.0
standby 10 ip 10.110.10.1
no shutdown

interface vlan 200
description "HR"
ip address 10.110.20.253 255.255.255.0
standby 10 ip 10.110.20.1
no shutdown

interface vlan 300
description "GUESTS"
ip address 10.110.30.253 255.255.255.0
standby 10 ip 10.110.30.1
no shutdown

interface vlan 400
description "IT"
ip address 10.110.100.253 255.255.255.0
standby 10 ip 10.110.100.1
no shutdown

interface g0/0
description "Uplink to R2"
no switchport
ip address 10.112.110.2 255.255.255.0
no shutdown

interface loop 0
ip address 1.1.3.3 255.255.255.255

router ospf 1
default-information originate
network 1.1.3.3 0.0.0.0 area 0
network 10.110.10.0 0.0.0.255 area 0
network 10.110.20.0 0.0.0.255 area 0
network 10.110.30.0 0.0.0.255 area 0
network 10.110.100.0 0.0.0.255 area 0
passive-interface vlan 100
passive-interface vlan 200
passive-interface vlan 300
passive-interface vlan 400
exit



```


# ASW1

```
enable
configure terminal
hostname Access-Switch1
ip domain-lookup
ip name-server 8.8.8.8

interface loop 0
ip address 1.1.3.4 255.255.255.255

interface range g0/2-3
switchport access vlan 100
no shut
exit

interface range g0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit

router ospf 1
network 1.1.3.4 0.0.0.0 area 0

vtp domain ccnp


end


```

# ASW2

```
enable
configure terminal
hostname Access-Switch2
interface range g0/2-3
switchport access vlan 200
no shutdown
exit

interface loop 0
ip address 1.1.3.5 255.255.255.255

interface range g0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit

router ospf 1
network 1.1.3.5 0.0.0.0

```

# ASW3

```
enable
configure terminal
hostname Access-Switch3
interface range g0/2-3
switchport access vlan 300
no shutdown
exit

interface loop 0
ip address 1.1.3.6 255.255.255.255

interface range g0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit

router ospf 1
network 1.1.3.5 0.0.0.0 area 0










```

# ASW4

```
enable
configure terminal
hostname Access-Switch4
interface range g0/2-3
switchport access vlan 400
no shutdown
exit

interface loop 0
ip address 1.1.3.7 255.255.255.0

interface range g0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit

router ospf 1
network 1.1.3.7 0.0.0.0 area 0


```




################### REMOTE SITE #########################



# Remote Datacenter 2 servers

# Server windows 2022 fresh install

```


# Server01
ip 10.100.100.10
ip 10.100.100.11

# Server02
ip 10.100.100.20
ip 10.100.100.21


```

# R3 

```
enable
configure terminal 
hostname R3
ip name-server 8.8.8.8
ip routing
ip multicast-routing distributed

interface loop 0
ip address 1.1.4.1 255.255.255.255
ip ospf 1 area 0

interface loop 1
ip address 1.1.41.1 255.255.255.255
ip ospf 1 area 0

interface loop 2
ip address 1.1.41.2 255.255.255.255
ip ospf 1 area 0

interface g1
description "Link to ISP"
ip nat outside
ip address 172.16.13.2 255.255.255.0
no shutdown

interface g2
description "Link to DCSW1"
ip address 10.1.1.1 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
no shutdown

interface g3
description "Link to DCSW2"
ip address 10.1.2.1 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
no shutdown

interface g4
description "Link to DCSW3"
ip address 10.1.3.1 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
no shutdown

interface g5
description "Link to DCSW4"
ip address 10.1.4.1 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
no shutdown

router ospf 1
router-id 1.1.4.1

router bgp 65001
template peer-policy RR-PP
route-reflector-client
send-community both
exit-peer-policy

template peer-session RR-PS
remote-as 65001
update-source Loopback0
exit-peer-session

bgp router-id 1.1.4.1
bgp log-neighbor-changes
no bgp default ipv4-unicast
neighbor 1.1.4.2 remote-as 65001
neighbor 1.1.4.2 update-source Loopback0
neighbor 1.1.4.3 inherit peer-session RR-PS
neighbor 1.1.4.4 inherit peer-session RR-PS

address-family ipv4
exit-address-family

address-family l2vpn evpn
neighbor 1.1.4.2 activate
neighbor 1.1.4.2 send-community both
neighbor 1.1.4.3 activate
neighbor 1.1.4.3 send-community extended
neighbor 1.1.4.3 inherit peer-policy RR-PP
neighbor 1.1.4.4 activate
neighbor 1.1.4.4 send-community extended
neighbor 1.1.4.4 inherit peer-policy RR-PP
exit-address-family

ip pim rp-addres 1.1.41.2
ip msdp peer 1.1.42.2 connect-source
loopback1 remote-as 65001
ip msdp cache-sa-state

interface tunnel 1
ip address 192.168.10.2 255.255.255.0
tunnel source 172.16.13.2
tunnel destination 172.16.12.2
exit

router eigrp 10
no auto-summary
network 192.168.10.0
exit

access-list 10 permit any
ip nat inside source list 10 interface g1 overload

ip route 0.0.0.0 0.0.0.0 g1 172.16.13.1

interface range g2-5
description "links to DCSW1-4"
ip nat inside
exit




```

# R4 

```
enable
configure terminal 
hostname R4
ip name-server 8.8.8.8
ip routing
ip multicast-routing distributed


interface loop 0
ip address 1.1.4.1 255.255.255.255
ip ospf 1 area 0

interface loop 1
ip address 1.1.42.1 255.255.255.255
ip ospf 1 area 0

interface loop 2
ip address 1.1.42.2 255.255.255.255
ip ospf 1 area 0

ip pim sparse-mode
ip ospf 1 area 0


interface g1
description "Link to ISP"
ip nat outside
ip address 172.16.14.2 255.255.255.0
no shutdown

interface g2
description "Link to DCSW1"
ip address 10.2.1.1 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
no shutdown

interface g3
description "Link to DCSW2"
ip address 10.2.2.1 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
no shutdown

interface g4
description "Link to DCSW3"
ip address 10.2.3.1 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
no shutdown

interface g5
description "Link to DCSW4"
ip address 10.2.4.1 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
no shutdown

router ospf 1
router-id 1.1.4.2

router bgp 65001
template peer-policy RR-PP
route-reflector-client
send-community both
exit-peer-policy

template peer-session RR-PS
remote-as 65001
update-source Loopback0
exit-peer-session

bgp router-id 1.1.4.2
bgp log-neighbor-changes
no gp default ipv4-unicast
neighbor 1.1.4.1 remote-as 65001
neighbor 1.1.4.1 update-source loopback0
neighbor 1.1.4.2 inherit peer-session RR-PS
neighbor 1.1.4.3 inherit peer-session RR-PS

address-family ipv4
exit-address-family

address-family l2vpn evpn
neighbor 1.1.4.1 activate
neighbor 1.1.4.1 send-community both
neighbor 1.1.4.3 activate
neighbor 1.1.4.3 send-community extended
neighbor 1.1.4.3 inherit peer-policy RR-PP
neighbor 1.1.4.4 activate
neighbor 1.1.4.4 send-community extended
neighbor 1.1.4.4 inherit peer-policy RR-PP
exit-address-family

ip pim rp-address 1.1.42.1
ip msdp peer 172.16.254.1 connect-source loopback1
remote-as 65001
ip msdp cache-sa-state


interface tunnel 1
ip address 192.168.20.2 255.255.255.0
tunnel source 172.16.13.2
tunnel destination 172.16.12.2
exit

router eigrp 20
no auto-summary
network 192.168.20.0
exit

access-list 10 permit any
ip nat inside source list 10 interface g1 overload

ip route 0.0.0.0 0.0.0.0 g1 172.16.14.1

interface range g2-5
ip nat inside
exit


end


```

# DCSW1 

```
enable
configure terminal
vtp domain ccnp
hostname DCSW1

vrf definition green
rd 1:1
!
address-family ipv4
route-target export 1:1
route-target import 1:1
route-target export 1:1 stitching
route-target import 1:1 stitching
exit-address-family
!
address-family ipv6
route-target export 1:1
route-target import 1:1
route-target export 1:1 stitching
route-target import 1:1 stitching
exit-address-family

ip routing

ip multicast-routing

l2vpn evpn
replication-type static
router-id Loopback1
default-gateway advertise

l2vpn evpn instance 101 vlan-based
encapsulation vxlan
replication-type static

l2vpn evpn instance 102 vlan-based
encapsulation vxlan
replication-type ingress

vlan configuration 101
member evpn-instance 101 vni 10101
vlan configuration 102
member evpn-instance 102 vni 10102
vlan configuration 901
member vni 50901

interface Loopback0
ip address 1.1.4.3 255.255.255.255
ip ospf 1 area 0

interface Loopback1
ip address 1.1.43.1 255.255.255.255
ip pim sparse-mode
ip ospf 1 area 0




interface g0/0
description "Link to R3"
no switchport
ip address 10.1.1.2 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
no shutdown

interface g0/2
description "Link to R4"
no switchport
ip address 10.2.1.1 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
no shutdown

interface GigabitEthernet0/2
switchport mode trunk
!
interface Vlan101
vrf forwarding green
ip address 10.1.101.1 255.255.255.0
!
interface Vlan102
vrf forwarding green
ip address 10.1.102.1 255.255.255.0
!
interface Vlan901
vrf forwarding green
ip unnumbered Loopback1
ipv6 enable
no autostate
!
interface nve1
no ip address
source-interface Loopback1
host-reachability protocol bgp
member vni 10101 mcast-group 225.0.0.101
member vni 10102 ingress-replication
member vni 50901 vrf green

router ospf 1
router-id 1.1.4.3

bgp log-neighbor-changes
no bgp default ipv4-unicast
neighbor 1.1.4.1 remote-as 65001
neighbor 1.1.4.1 update-source Loopback0
neighbor 1.1.4.2 remote-as 65001
neighbor 1.1.4.2 update-source Loopback0

address-family ipv4
exit-address-family

address-family l2vpn evpn
neighbor 1.1.4.1 activate
neighbor 1.1.4.1 send-community both
neighbor 1.1.4.2 activate
neighbor 1.1.4.2 send-community both
exit-address-family

address-family ipv4 vrf green
advertise l2vpn evpn
redistribute connected
redistribute static
exit-address-family
!
address-family ipv6 vrf green
redistribute connected
redistribute static
advertise l2vpn evpn
exit-address-family
!
ip pim rp-address 1.1.42.2
end


```

# DCSW2 

```
enable
configure terminal
hostname DCSW2





vrf definition green
rd 1:1
!
address-family ipv4
route-target export 1:1
route-target import 1:1
route-target export 1:1 stitching
route-target import 1:1 stitching
exit-address-family
!
address-family ipv6
route-target export 1:1
route-target import 1:1
route-target export 1:1 stitching
route-target import 1:1 stitching
exit-address-family
!
ip routing
!
ip multicast-routing
!
l2vpn evpn
replication-type static
router-id Loopback1
default-gateway advertise
!
l2vpn evpn instance 101 vlan-based
encapsulation vxlan
!
l2vpn evpn instance 102 vlan-based
encapsulation vxlan
replication-type ingress
!
vlan configuration 101
member evpn-instance 101 vni 10101
vlan configuration 102
member evpn-instance 102 vni 10102
vlan configuration 901
member vni 50901
!
interface Loopback0
ip address 1.1.4.4 255.255.255.255
ip ospf 1 area 0
!
interface Loopback1
ip address 1.1.44.1 255.255.255.255
ip pim sparse-mode
ip ospf 1 area 0
!


interface g0/0 
no switchport
ip address 10.1.1.2 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
no shutdown
exit

interface g0/1
no switchport
ip address 10.2.1.2 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
no shutdown

interface g0/2
switchport mode trunk


interface Vlan101
vrf forwarding green
ip address 10.1.101.1 255.255.255.0

interface Vlan102
vrf forwarding green
ip address 10.1.102.1 255.255.255.0

interface Vlan901
vrf forwarding green
ip unnumbered Loopback1
ipv6 enable
no autostate

interface nve1
no ip address
source-interface Loopback1
host-reachability protocol bgp
member vni 10101 mcast-group 225.0.0.101
member vni 50901 vrf green
member vni 10102 ingress-replication

router ospf 1
router-id 172.16.255.4

router bgp 65001
bgp log-neighbor-changes
no bgp default ipv4-unicast
neighbor 1.1.4.1 remote-as 65001
neighbor 1.1.4.1 update-source Loopback0
neighbor 1.1.4.2 remote-as 65001
neighbor 1.1.4.2 update-source Loopback0

address-family ipv4
exit-address-family

address-family l2vpn evpn
neighbor 1.1.4.1 activate
neighbor 1.1.4.1 send-community both
neighbor 1.1.4.2 activate
neighbor 1.1.4.2 send-community both
exit-address-family

address-family ipv4 vrf green
advertise l2vpn evpn
redistribute connected
redistribute static
exit-address-family

address-family ipv6 vrf green
redistribute connected
redistribute static
advertise l2vpn evpn
exit-address-family

ip pim rp-address 1.1.42.2

end


```

# SW5 

```
enable
configure terminal
hostname SW5
interface g0/0 
no switchport
ip address 14.1.3.2 255.255.255.0
no shutdown
exit

interface range g0/1-2
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit

interface port-channel 20
no switchport
ip address 14.1.20.2 255.255.255.0
no shutdown
exit

interface range g1/2-3
shutdown
no switchport
channel-group 20 mode on 
no shutdown
exit

interface port-channel 30
no switchport
ip address 14.1.30.1 255.255.255.0
no shutdown
exit

interface range g2/0-1
shutdown
no switchport
channel-group 30 mode on 
no shutdown
exit

interface vlan 50
ip address 50.1.1.253 255.255.255.0
standby 10 ip 50.1.1.1
no shutdown
exit

router ospf 1
network 14.1.0.0 0.0.255.255 area 0
network 50.1.1.0 0.0.0.255 area 0
passive-interface vlan 50
exit
end
wr

```

# SW6 

```
enable
configure terminal
hostname SW6
interface g0/0 
no switchport
ip address 14.1.4.2 255.255.255.0
no shutdown
exit

interface range g0/1-2
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit

interface port-channel 30
no switchport
ip address 14.1.30.2 255.255.255.0
no shutdown
exit

interface range g2/0-1
shutdown
no switchport
channel-group 30 mode on 
no shutdown
exit

interface vlan 50
ip address 50.1.1.254 255.255.255.0
standby 10 ip 50.1.1.1
no shutdown
exit

router ospf 1
network 14.1.0.0 0.0.255.255 area 0
network 50.1.1.0 0.0.0.255 area 0
passive-interface vlan 50
exit
end
wr


```

# Access-Switch5

```
enable
configure terminal
hostname Access-Switch5

interface g1/0 
switchport access vlan 50
no shutdown
exit

interface range g0/0-3
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit

router ospf 1
network 14.1.0.0 0.0.255.255 area 0
network 50.1.1.0 0.0.0.255 area 0
passive-interface vlan 50
exit
end
wr

```

# Access-Switch6

```
enable
configure terminal
hostname Access-Switch6

interface range g1/0-1
switchport access vlan 50
no shutdown
exit

interface range g0/0-3
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit

router ospf 1
network 14.1.0.0 0.0.255.255 area 0
network 50.1.1.0 0.0.0.255 area 0
passive-interface vlan 50
exit
end
wr
```
