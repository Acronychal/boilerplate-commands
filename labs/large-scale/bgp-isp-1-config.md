# lab
# screenshot
# 


# BGP-01
```
configure terminal
hostname BGP-R1
ip domain-lookup
ip name-server 8.8.8.8


interface g0/0
no shut
ip address dhcp
ip nat outside
interface g0/1
no shut
ip address 172.16.1.1 255.255.255.0
ip nat inside
int loop 0
ip address 1.1.1.1 255.255.255.255
exit

access-list 1 permit any
ip nat inside source list 1 interface g0/0 overload


router bgp 65000
default-information originate
redistribute connected
redistribute static
neighbor 1.1.1.2 remote-as 65000
neighbor 1.1.1.2 update-source loopback 0

exit
ip route 0.0.0.0 0.0.0.0 192.168.122.1

router ospf 1
network 1.1.1.0 0.0.0.255 area 0 
network 172.16.1.0 0.0.0.255 area 0
end




```
# BGP-02
```
configure terminal
hostname BGP-R2
ip domain-lookup
ip name-server 8.8.8.8


interface g0/0
no shutdown
ip address 172.16.1.2 255.255.255.0
interface g0/1
no shutdown
ip address 172.16.2.1 255.255.255.0
int loop 0
ip address 1.1.1.2 255.255.255.255
exit


router bgp 65000
neighbor 1.1.1.1 remote-as 65000
neighbor 1.1.1.3 remote-as 65000

network 1.1.1.1 mask 255.255.255.255
network 172.16.1.0 mask 255.255.255.0
network 172.16.2.0 mask 255.255.255.0
default-information originate
redistribute connected
redistribute static

router ospf 1
network 0.0.0.0 255.255.255.255 area 0 
end


```
# BGP-03
```
configure terminal
hostname BGP-R3
ip domain-lookup
ip name-server 8.8.8.8
ip route 0.0.0.0 0.0.0.0 172.16.2.1

interface g0/0
no shut
ip address 172.16.2.2 255.255.255.0
interface g0/1
ip address 172.16.3.1 255.255.255.0
no shut
interface g0/2
ip address 172.16.6.1 255.255.255.0
no shut
interface g0/3
ip address 172.16.11.1 255.255.255.0
no shut
int loop 0
ip address 1.1.1.3 255.255.255.255
exit

router ospf 1
network 0.0.0.0 0.0.0.0 area 0
default-information originate
redistribute connected
redistribute static




router bgp 65000

network 1.1.1.3 mask 255.255.255.255
network 172.16.2.0 mask 255.255.255.0
network 172.16.3.0 mask 255.255.255.0
network 172.16.6.0 mask 255.255.255.0
network 172.16.11.0 mask 255.255.255.0

neighbor 1.1.1.2 remote-as 65000
neighbor 1.1.1.4 remote-as 65000
neighbor 1.1.1.5 remote-as 65000
neighbor 1.1.1.6 remote-as 65000
neighbor 1.1.1.2 update-source loopback 0
neighbor 1.1.1.4 update-source loopback 0
neighbor 1.1.1.5 update-source loopback 0
neighbor 1.1.1.6 update-source loopback 0
neighbor 1.1.1.2 route-reflector-client
neighbor 1.1.1.4 route-reflector-client
neighbor 1.1.1.5 route-reflector-client
neighbor 1.1.1.6 route-reflector-client




```
# BGP-04
```
configure terminal
hostname BGP-R4
ip domain-lookup
ip name-server 8.8.8.8

interface g0/0
ip address 172.16.3.2 255.255.255.0
no shutdown
interface g0/1
ip address 172.16.4.1 255.255.255.0
no shutdown
interface g0/2
ip address 172.16.7.1 255.255.255.0
no shutdown
interface loop 0
ip address 1.1.1.4 255.255.255.255


router bgp 65000

network 1.1.1.4 mask 255.255.255.255
network 172.16.7.0 mask 255.255.255.0
network 172.16.3.0 mask 255.255.255.0
network 172.16.4.0 mask 255.255.255.0

neighbor 1.1.1.3 remote-as 65000
neighbor 1.1.1.5 remote-as 65000

router ospf 1
network 0.0.0.0 0.0.0.0 area 0
default-information originate
redistribute connected
redistribute static


```
# BGP-05
```

configure terminal
hostname BGP-R5
ip domain-lookup
ip name-server 8.8.8.8

interface g0/0
ip address 172.16.4.2 255.255.255.0
no shutdown
interface g0/1
ip address 172.16.5.1 255.255.255.0
no shutdown
interface g0/2
ip address 172.16.8.1 255.255.255.0
no shutdown
interface g0/3
ip address 172.16.11.2 255.255.255.0
no shutdown
interface loop 0
ip address 1.1.1.5 255.255.255.255

router bgp 65000
network 1.1.1.5 mask 255.255.255.255
network 172.16.11.0 mask 255.255.255.0
network 172.16.8.0 mask 255.255.255.0
network 172.16.4.0 mask 255.255.255.0
network 172.16.5.0 mask 255.255.255.0

neighbor 1.1.1.3 remote-as 65000
neighbor 1.1.1.4 remote-as 65000
neighbor 1.1.1.6 remote-as 65000
neighbor 1.1.1.9 remote-as 65000

router ospf 1
network 0.0.0.0 0.0.0.0 area 0
default-information originate
redistribute connected
redistribute static


```

# BGP-06

```

configure terminal
hostname BGP-R6
ip domain-lookup
ip name-server 8.8.8.8

interface g0/0
ip address 172.16.5.2 255.255.255.0
no shutdown
interface g0/1
ip address 172.16.6.2 255.255.255.0
no shutdown
interface g0/2
ip address 172.16.10.1 255.255.255.0
no shutdown
interface g0/3
ip address 172.16.9.1 255.255.255.0
no shutdown 
interface loop 0
ip address 1.1.1.6 255.255.255.255



router bgp 65000
network 1.1.1.6 mask 255.255.255.255
network 172.16.5.0 mask 255.255.255.0
network 172.16.6.0 mask 255.255.255.0
network 172.16.9.0 mask 255.255.255.0
network 172.16.10.0 mask 255.255.255.0

neighbor 1.1.1.3 remote-as 65000
neighbor 1.1.1.5 remote-as 65000
neighbor 1.1.1.7 remote-as 65000
neighbor 1.1.1.8 remote-as 65000

router ospf 1
network 0.0.0.0 0.0.0.0 area 0
default-information originate
redistribute connected
redistribute static




```
# BGP-07
```
configure
set system host-name BGP-R7
set system name-server 8.8.8.8

set interfaces ethernet eth0 address 172.16.10.2/24
set interfaces ethernet eth0 duplex auto
set interfaces ethernet eth0 speed auto
set interfaces loopback lo address 1.1.1.7/32

set protocols bgp 65000 neighbor 1.1.1.6 remote-as 65000
set protocols bgp 65000 neighbor 1.1.1.6 update-source 1.1.1.7
set protocols bgp 65000 neighbor 1.1.1.6 ebgp-multihop 2
set protocols bgp 65000 address-family ipv4-unicast network 1.1.1.7/32
set protocols bgp 65000 address-family ipv4-unicast network 172.16.10.0/24
set protocols bgp 65000 parameters router-id 1.1.1.7

commit
save
exit





```


# BGP-08
```
configure
set system host-name BGP-R8
set system name-server 8.8.8.8

set interfaces ethernet eth0 address 172.16.9.2/24
set interfaces ethernet eth0 duplex auto
set interfaces ethernet eth0 speed auto
set interfaces loopback lo address 1.1.1.8/32

set protocols bgp 65000 neighbor 1.1.1.6 remote-as 65000
set protocols bgp 65000 neighbor 1.1.1.6 update-source 1.1.1.8
set protocols bgp 65000 neighbor 1.1.1.6 ebgp-multihop 2
set protocols bgp 65000 address-family ipv4-unicast network 1.1.1.8/32
set protocols bgp 65000 address-family ipv4-unicast network 172.16.9.0/24
set protocols bgp 65000 parameters router-id 1.1.1.8

configure
set protocols ospf area 0 network 172.16.9.0/24
set protocols ospf area 0 network 172.16.12.0/24
set protocols ospf parameters router-id 1.1.1.8
set protocols ospf redistribute bgp





commit
save
exit


```


# BGP-09
```
configure terminal
hostname BGP-R9
ip name-server 8.8.8.8
ip route 0.0.0.0/0 172.16.8.1

interface loopback 0
ip address 1.1.1.9/32

interface ethernet 1/1/1
no shutdown
no switchport
ip address 172.16.8.2/24

interface ethernet 1/1/2
no shutdown
no switchport
ip address 172.16.13.1/24

interface ethernet 1/1/3
no shutdown
no switchport
ip address 172.16.14.1/24


router bgp 65000
router-id 1.1.1.9
neighbor 1.1.1.5 

router ospf 1
router-id 1.1.1.9
default-information originate


exit
write memory





```

