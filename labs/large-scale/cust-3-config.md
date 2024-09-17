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




spanning-tree mode rapid-pvst
spanning-tree loopguard default






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
network 1.1.3.4 0.0.0.255 area 0

vtp domain ccnp

spanning-tree mode rapid-pvst
spanning-tree loopguard default



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

interface range g0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit
end



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

interface range g0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit
end
wr

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

interface range g0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit
end
wr


```




################### REMOTE SITE #########################



# Clients & Servers

# Server

```
ip 50.1.1.20/24 50.1.1.1

# Server1
ip 50.1.1.21/24 50.1.1.1

# Tiny-Client
ip 50.1.1.10/24 50.1.1.1

```

# R2 

```
configure terminal 
hostname R2
interface g0/4
ip address 2.2.2.1 255.255.255.0
no shutdown
exit

interface g0/0
ip address 14.1.1.1 255.255.255.0
no shutdown
exit

interface g0/1
ip address 14.1.2.1 255.255.255.0
no shutdown
exit

interface g0/2
ip address 14.1.3.1 255.255.255.0
no shutdown
exit

interface g0/3
ip address 14.1.4.1 255.255.255.0
no shutdown
exit

router ospf 1
network 14.1.0.0 0.0.255.255 area 0
default-information originate

interface tunnel 1
ip address 192.168.10.2 255.255.255.0
tunnel source 2.2.2.1
tunnel destination 1.1.1.1
exit

router eigrp 10
no auto-summary
network 192.168.10.0
exit

access-list 10 permit any
ip nat inside source list 10 interface g0/4 overload

ip route 0.0.0.0 0.0.0.0 g0/4 2.2.2.2

interface range g0/0-3
ip nat inside
exit

interface g0/4
ip nat outside
exit
end
wr

```

# SW3 

```
enable
configure terminal
vtp domain ccnp
hostname SW3
interface g0/0 
no switchport
ip address 14.1.1.2 255.255.255.0
no shutdown
exit

vlan 50
exit

interface vlan 50
ip address 50.1.1.251 255.255.255.0
standby 10 ip 50.1.1.1
no shutdown
exit

interface range g0/1-2
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit

interface port-channel 10
no switchport
ip address 14.1.10.1 255.255.255.0
no shutdown
exit

interface range g1/0-1
shutdown
no switchport
channel-group 10 mode on 
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

# SW4 

```
enable
configure terminal
hostname SW4
interface g0/0 
no switchport
ip address 14.1.2.2 255.255.255.0
no shutdown
exit

interface range g0/1-2
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit

interface port-channel 10
no switchport
ip address 14.1.10.2 255.255.255.0
no shutdown
exit

interface range g1/0-1
shutdown
no switchport
channel-group 10 mode on 
no shutdown
exit

interface port-channel 20
no switchport
ip address 14.1.20.1 255.255.255.0
no shutdown
exit

interface range g1/2-3
shutdown
no switchport
channel-group 20 mode on 
no shutdown
exit

interface vlan 50
ip address 50.1.1.252 255.255.255.0
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
