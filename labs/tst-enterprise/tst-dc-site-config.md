## This is the configuration for DC Site (AS65500)

# SP-01

```
configure terminal
hostname SP-01
default interface eth1/1-4

feature ospf

interface e1/1
description "Link to LF-01"
no switchport
ip address 10.1.1.1/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown

interface eth1/2
description "Link to LF-02"
no switchport
ip address 10.1.2.1/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown

interface eth1/3
description "Link to LF-03"
no switchport
ip address 10.1.3.1/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown

interface eth1/4
description "Link to LF-04"
no switchport
ip address 10.1.4.1/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown

router ospf 1
exit



```

# SP-02

```
configure terminal
hostname SP-02
default interface eth1/1-4

feature ospf

interface e1/1
description "Link to LF-01"
no switchport
ip address 10.2.1.1/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown

interface eth1/2
description "Link to LF-02"
no switchport
ip address 10.2.2.1/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown

interface eth1/3
description "Link to LF-03"
no switchport
ip address 10.2.3.1/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown

interface eth1/4
description "Link to LF-04"
no switchport
ip address 10.2.4.1/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown

router ospf 1
exit


```

## LF-01

```
configure terminal
hostname LF-01
default interface eth 1/1-2

feature ospf

interface eth1/1
description "Link to SP-01"
no switchport
ip address 10.1.1.0/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown

interface eth1/2
description "Link to SP-02"
no switchport
ip address 10.2.2.0/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown
exit

interface loopback 0
ip address 100.1.1.1/32
ip router ospf 1 area 0
exit

router ospf 1
exit


feature nv overlay
interface nve 1
no shutdown
source-interface loopback 0
exit

feature vn-segment-vlan-based

vlan 100
vn-segment 5100
exit


interface nve 1
member vni 5100
ingress-replication protocol static
peer-ip 100.4.4.4
exit





```

## LF-02

```
configure terminal 
hostname LF-02
default interface eth 1/1-2

feature ospf

interface eth1/1
description "Link to SP-01"
no switchport
ip address 10.1.2.0/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown 

interface eth1/2
description "Link to SP-02"
no switchport
ip address 10.2.2.0/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown
exit

interface loopback 0
ip address 100.2.2.2/32
ip router ospf 1 area 0
exit

router ospf 1
exit


feature nv overlay


interface nve 1
no shutdown
source-interface loopback 0
exit

feature vn-segment-vlan-based

vlan 100
vn-segment 5100
exit




```



# LF-03

```
configure terminal 
hostname LF-03
default interface eth 1/1-2

feature ospf

interface eth1/1
description "Link to SP-01"
no switchport
ip address 10.1.3.0/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown 

interface eth1/2
description "Link to SP-02"
no switchport
ip address 10.2.3.0/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown
exit

interface loopback 0
ip address 100.3.3.3/32
ip router ospf 1 area 0
exit

router ospf 1
exit


feature nv overlay



interface nve 1
no shutdown
source-interface loopback 0
exit


feature vn-segment-vlan-based

vlan 100
vn-segment 5100
exit

```

# LF-04

```
configure terminal 
hostname LF-04
default interface e1/1-2,e1/8-9


feature ospf
feature pim
feature lacp



interface port-channel 1
no switchport
ip address 10.0.1.4/29
ip router ospf 1 area 0
ip ospf network point-to-point
no shutdown
exit

interface e1/8-9
no switchport
channel-group 1 mode on
no shutdown

exit

ip route 0.0.0.0 0.0.0.0 port-channel 1 10.0.1.1



interface eth1/1
description "Link to SP-01"
no switchport
ip address 10.1.4.0/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown 

interface eth1/2
description "Link to SP-02"
no switchport
ip address 10.2.4.0/31
ip ospf network point-to-point
ip router ospf 1 area 0
no shutdown
exit

interface loopback 0
ip address 100.4.4.4/32
ip router ospf 1 area 0
exit

router ospf 1
exit


feature nv overlay
interface nve 1
no shutdown
source-interface loopback 0
exit

feature vn-segment-vlan-based

vlan 100
vn-segment 5100
exit


```
# TST-OB-MGMT-SW-01

```

configure terminal
hostname tst-ob-mgmt-sw-01

ip dhcp pool spine

ip dhcp pool leaf



```