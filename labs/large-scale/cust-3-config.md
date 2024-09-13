# large enterprise with 2 sites connected via tunnel
- site one users
- site two servers admin


######### MAIN SITE ########


# VPC1-8 Configure according to vlan
ip <targetip/cidr> <gateway>

# VPC1
ip 10.1.1.10/24 10.1.1.1

# VPC2
ip 10.1.1.11/24 10.1.1.1

# VPC3
ip 20.1.1.10/24 20.1.1.1

# VP4
ip 20.1.1.11/24 20.1.1.1

# VPC5
ip 30.1.1.10/24 30.1.1.1

# VPC6
ip 30.1.1.11/24 30.1.1.1

# VPC7
ip 40.1.1.10/24 40.1.1.1

# VPC8
ip 40.1.1.11/24 40.1.1.1


# Internet Router

configure terminal
hostname Internet
interface loopback 1
ip address 8.8.8.8 255.255.255.0

interface g0/0
no shutdown
ip address 1.1.1.2 255.255.255.0
exit

interface g0/1
no shutdown
ip address 2.2.2.2 255.255.255.0
exit
end
wr






# Access-Switch1

enable
configure terminal
hostname Access-Switch1
interface range g0/2-3
switchport access vlan 10
no shut
exit

interface range g0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
no shut
exit

vtp domain ccnp
end
wr



# Access-Switch2

enable
configure terminal
hostname Access-Switch2
interface range g0/2-3
switchport access vlan 20
no shutdown
exit

interface range g0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit
end
wr



# Access-Switch3

enable
configure terminal
hostname Access-Switch3
interface range g0/2-3
switchport access vlan 30
no shutdown
exit

interface range g0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit
end
wr


# Access-Switch4

enable
configure terminal
hostname Access-Switch4
interface range g0/2-3
switchport access vlan 40
no shutdown
exit

interface range g0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
no shutdown
exit
end
wr


# SW1

enable
configure terminal
hostname SW1

int range g2/0-3
shutdown
no switchport
channel-group 10 mode on
no shutdown
exit


interface port-channel 10
ip address 11.1.1.1 255.255.255.0
no shutdown
exit

interface range g0/1-3, g1/0
switchport trunk encapsulation dot1q
switchport mode trunk
exit

vlan 10
exit
vlan 20
exit
vlan 30
exit
vlan 40
exit


interface vlan 10
no shutdown
ip add 10.1.1.254 255.255.255.0
standby 10 ip 10.1.1.1
exit

interface vlan 20
no shutdown
ip add 20.1.1.254 255.255.255.0
standby 10 ip 20.1.1.1
exit

interface vlan 30
no shutdown
ip add 30.1.1.254 255.255.255.0
standby 10 ip 30.1.1.1
exit

interface vlan 40
no shutdown
ip add 40.1.1.254 255.255.255.0
standby 10 ip 40.1.1.1
exit

interface g0/0
no switchport
ip address 12.1.1.1 255.255.255.0
no shutdown
exit

router ospf 1
network 12.1.1.0 0.0.0.255 area 0
network 10.1.1.0 0.0.0.255 area 0
network 20.1.1.0 0.0.0.255 area 0
network 30.1.1.0 0.0.0.255 area 0
network 40.1.1.0 0.0.0.255 area 0
passive-interface vlan 10
passive-interface vlan 20
passive-interface vlan 30
passive-interface vlan 40
exit

end
wr




# SW2


enable
configure terminal
hostname SW2

interface g0/0
no switchport
ip address 13.1.1.1 255.255.255.0
no shutdown

interface range g2/0-3
shutdown
no switchport
channel-group 10 mode on
no shutdown

interface port-channel 10
ip address 11.1.1.2 255.255.255.0
no shut

interface range g0/1-3, g1/0
switchport trunk encapsulation dot1q
switchport mode trunk
exit



interface vlan 10
no shutdown
ip add 10.1.1.253 255.255.255.0
standby 10 ip 10.1.1.1
exit

interface vlan 20
no shutdown
ip add 20.1.1.253 255.255.255.0
standby 10 ip 20.1.1.1
exit

interface vlan 30
no shutdown
ip add 30.1.1.253 255.255.255.0
standby 10 ip 30.1.1.1
exit

interface vlan 40
no shutdown
ip add 40.1.1.253 255.255.255.0
standby 10 ip 40.1.1.1
exit

router ospf 1
network 13.1.1.0 0.0.0.255 area 0
network 10.1.1.0 0.0.0.255 area 0
network 20.1.1.0 0.0.0.255 area 0
network 30.1.1.0 0.0.0.255 area 0
network 40.1.1.0 0.0.0.255 area 0
passive-interface vlan 10
passive-interface vlan 20
passive-interface vlan 30
passive-interface vlan 40
end
wr





# R1 


configure terminal
hostname R1
interface g0/0
ip address 12.1.1.2 255.255.255.0
no shutdown

interface g0/1
ip address 13.1.1.2 255.255.255.0
no shutdown

interface g0/2
ip address 1.1.1.1 255.255.255.252
no shutdown

router ospf 1
network 12.1.1.0 0.0.0.255 area 0
network 13.1.1.0 0.0.0.255 area 0
default-information originate


ip route 0.0.0.0 0.0.0.0 g0/2 1.1.1.2


ip access-list standard 10
permit any
ip nat inside source list 10 int g0/2 overload

interface g0/0
ip nat inside
exit

interface g0/1
ip nat inside
exit

interface g0/2
ip nat outside
exit

interface tunnel 1
ip address 192.168.10.1 255.255.255.0
tunnel source 1.1.1.1
tunnel destination 2.2.2.1
exit

router eigrp 10
network 192.168.10.0
exit

end
wr


################### REMOTE SITE #########################



# Clients & Servers

# Server
ip 50.1.1.20/24 50.1.1.1

# Server1
ip 50.1.1.21/24 50.1.1.1

# Tiny-Client
ip 50.1.1.10/24 50.1.1.1

# R2 

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



# SW3 

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




# SW4 

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





# SW5 

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


# SW6 

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



# Access-Switch5

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



# Access-Switch6

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