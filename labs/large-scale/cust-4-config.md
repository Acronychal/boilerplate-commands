# Spine One

hostname Spine-01
!
ip routing
!
ip multicast-routing
!
interface Loopback0
ip address 172.16.255.1 255.255.255.255
ip ospf 1 area 0
!
interface Loopback1
ip address 172.16.254.1 255.255.255.255
ip ospf 1 area 0
!
interface Loopback2
ip address 172.16.255.255 255.255.255.255
ip pim sparse-mode
ip ospf 1 area 0
!
interface GigabitEthernet1/0/1
no switchport
ip address 172.16.13.1 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
!
interface GigabitEthernet1/0/2
no switchport
ip address 172.16.14.1 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
!
router ospf 1
router-id 172.16.255.1
!
router bgp 65001
template peer-policy RR-PP
route-reflector-client
send-community both
exit-peer-policy
!
template peer-session RR-PS
remote-as 65001
update-source Loopback0
exit-peer-session
!
bgp router-id 172.16.255.1
bgp log-neighbor-changes
no bgp default ipv4-unicast
neighbor 172.16.255.2 remote-as 65001
neighbor 172.16.255.2 update-source Loopback0
neighbor 172.16.255.3 inherit peer-session RR-PS
neighbor 172.16.255.4 inherit peer-session RR-PS
!
address-family ipv4
exit-address-family
!
address-family l2vpn evpn
neighbor 172.16.255.2 activate
neighbor 172.16.255.2 send-community both
neighbor 172.16.255.3 activate
neighbor 172.16.255.3 send-community extended
neighbor 172.16.255.3 inherit peer-policy RR-PP
neighbor 172.16.255.4 activate
neighbor 172.16.255.4 send-community extended
neighbor 172.16.255.4 inherit peer-policy RR-PP
exit-address-family
!
ip pim rp-address 172.16.255.255
ip msdp peer 172.16.254.2 connect-source Loopback1 remote-as 65001
ip msdp cache-sa-state
!
end


# Spine Two

hostname Spine-02
!
ip routing
!
ip multicast-routing
!
interface Loopback0
ip address 172.16.255.2 255.255.255.255
ip ospf 1 area 0
!
interface Loopback1
ip address 172.16.254.2 255.255.255.255
ip ospf 1 area 0
!
interface Loopback2
ip address 172.16.255.255 255.255.255.255
ip pim sparse-mode
ip ospf 1 area 0
!
interface GigabitEthernet1/0/1
no switchport
ip address 172.16.23.2 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
!
interface GigabitEthernet1/0/2
no switchport
ip address 172.16.24.2 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
!
router ospf 1
router-id 172.16.255.2
!
router bgp 65001
template peer-policy RR-PP
route-reflector-client
send-community both
exit-peer-policy
!
template peer-session RR-PS
remote-as 65001
update-source Loopback0
exit-peer-session
!
bgp router-id 172.16.255.2
bgp log-neighbor-changes
no bgp default ipv4-unicast
neighbor 172.16.255.1 remote-as 65001
neighbor 172.16.255.1 update-source Loopback0
neighbor 172.16.255.3 inherit peer-session RR-PS
neighbor 172.16.255.4 inherit peer-session RR-PS
!
address-family ipv4
exit-address-family
!

address-family l2vpn evpn
neighbor 172.16.255.1 activate
neighbor 172.16.255.1 send-community both
neighbor 172.16.255.3 activate
neighbor 172.16.255.3 send-community extended
neighbor 172.16.255.3 inherit peer-policy RR-PP
neighbor 172.16.255.4 activate
neighbor 172.16.255.4 send-community extended
neighbor 172.16.255.4 inherit peer-policy RR-PP
exit-address-family
!
ip pim rp-address 172.16.255.255
ip msdp peer 172.16.254.1 connect-source Loopback1 remote-as 65001
ip msdp cache-sa-state
!
end

# Leaf One

hostname Leaf-01
!
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
replication-type static
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
ip address 172.16.255.3 255.255.255.255
ip ospf 1 area 0
!
interface Loopback1
ip address 172.16.254.3 255.255.255.255
ip pim sparse-mode
ip ospf 1 area 0
!
interface GigabitEthernet1/0/1
no switchport
ip address 172.16.13.3 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
!
interface GigabitEthernet1/0/2
no switchport
ip address 172.16.23.3 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
!
interface GigabitEthernet1/0/10
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
!
router ospf 1
router-id 172.16.255.3
!
router bgp 65001
bgp log-neighbor-changes
no bgp default ipv4-unicast
neighbor 172.16.255.1 remote-as 65001
neighbor 172.16.255.1 update-source Loopback0
neighbor 172.16.255.2 remote-as 65001
neighbor 172.16.255.2 update-source Loopback0
!
address-family ipv4
exit-address-family
!
address-family l2vpn evpn
neighbor 172.16.255.1 activate
neighbor 172.16.255.1 send-community both
neighbor 172.16.255.2 activate
neighbor 172.16.255.2 send-community both
exit-address-family
!
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
ip pim rp-address 172.16.255.255
!
end

# Leaf Two

hostname Leaf-02
!
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
ip address 172.16.255.4 255.255.255.255
ip ospf 1 area 0
!
interface Loopback1
ip address 172.16.254.4 255.255.255.255
ip pim sparse-mode
ip ospf 1 area 0
!
interface GigabitEthernet1/0/1
no switchport
ip address 172.16.14.4 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
!
interface GigabitEthernet1/0/2
no switchport
ip address 172.16.24.4 255.255.255.0
ip pim sparse-mode
ip ospf network point-to-point
ip ospf 1 area 0
!
interface GigabitEthernet1/0/10
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
member vni 50901 vrf green
member vni 10102 ingress-replication
!
router ospf 1
router-id 172.16.255.4
!
router bgp 65001
bgp log-neighbor-changes
no bgp default ipv4-unicast
neighbor 172.16.255.1 remote-as 65001
neighbor 172.16.255.1 update-source Loopback0
neighbor 172.16.255.2 remote-as 65001
neighbor 172.16.255.2 update-source Loopback0
!
address-family ipv4
exit-address-family
!
address-family l2vpn evpn
neighbor 172.16.255.1 activate
neighbor 172.16.255.1 send-community both
neighbor 172.16.255.2 activate
neighbor 172.16.255.2 send-community both
exit-address-family
!
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
ip pim rp-address 172.16.255.255
!
end
