# Customer 1 configuration template

# Notes 
  - loop back schema 1.1.2.x/32
  - Vlans = staff, guest, it, mgmt. 

# R1
```

configure terminal
hostname R1
ip domain-lookup
ip name-server 8.8.8.8
ip route 0.0.0.0 0.0.0.0 172.16.7.1


interface g0/0
description "External to ISP"
ip address 172.16.7.2 255.255.255.0
ip nat outside
no shutdown
interface g0/1
description "Trunk to S1"
ip nat inside
no shutdown
interface g0/1.10
description "Staff"
encapsulation dot1Q 10
ip address 10.1.10.1 255.255.255.0
ip nat inside
no shutdown
interface g0/1.20
description "Guest"
encapsulation dot1Q 20
ip address 10.1.20.1 255.255.255.0
ip nat inside
no shutdown
interface g0/1.30
description "IT"
encapsulation dot1Q 30
ip address 10.1.30.1 255.255.255.0
no shutdown
interface g0/1.100
description "MGMT"
encapsulation dot1Q 100
ip address 10.1.100.1 255.255.255.0
no shutdown
interface loop 0
ip address 1.1.2.1 255.255.255.255
exit

access-list 1 permit 10.1.10.0 0.0.0.255
access-list 1 permit 10.1.20.0 0.0.0.255
access-list 1 permit 10.1.30.0 0.0.0.255
access-list 1 permit 10.1.100.0 0.0.0.255
ip nat inside source list 1 interface g0/0 overload


ip dhcp pool vlan10
network 10.1.10.0 255.255.255.0
default-router 10.1.10.1
dns-server 8.8.8.8

ip dhcp pool vlan20
network 10.1.20.0 255.255.255.0
default-router 10.1.20.1
dns-server 8.8.8.8

ip dhcp pool vlan30
network 10.1.30.0 255.255.255.0
default-router 10.1.30.1
dns-server 8.8.8.8

ip dhcp pool vlan100
network 10.1.100.0 255.255.255.0
default-router 10.1.100.1
dns-server 8.8.8.8






```


# S1

```
enable
configure terminal
hostname S1
int g0/0
description "Trunk to R1"
switchport
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan all
no shutdown
exit
vlan 10
vlan 20
vlan 30
vlan 100
interface vlan 10 
description "Staff"
ip address 10.1.10.254 255.255.255.0
no shutdown
interface vlan 20
description "Guests"
ip address 10.1.20.254 255.255.255.0
no shutdown
interface vlan 30
description "IT"
ip address 10.1.30.254 255.255.255.0
no shutdown
interface vlan 100
description "MGMT"
ip address 10.1.100.254 255.255.255.0
no shutdown
interface loop 0
ip address 1.1.2.2 255.255.255.255


interface g0/1
description "Staff"
switchport access vlan 10
no shutdown
interface g0/2
description "Guests"
switchport access vlan 20
no shutdown
interface g0/3
description "IT"
switchport access vlan 30
no shutdown
interface g1/0
description "MGMT"
switchport access vlan 100
no shutdown 
exit
ip route 0.0.0.0 0.0.0.0 172.16.7.1
router ospf 1
network 0.0.0.0 0.0.0.0 area 0
exit

