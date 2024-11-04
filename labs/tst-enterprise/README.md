## Modeling Lab for Small Enterprise 
- Modeling Platform: GNS3 on bare metal (Dell R630)

- Site Breakdown:
  - corporate datacenter 
    - 2 pfsense HA firewalls
    - 2 nexus-os virtual switch as spine
    - 4 nexus-os leaf/tor switches - 1 configured as edge leaf
    - 4 proxmox type-1 hypervisor 3 node cluster / 1 sandbox
    - 1 proxmox backbup server
    - 1 truenas nfs storage server
    - 1 iosv management switch 
    - 1 iosv out of band management switch
    - 1 windows 11 sys admin node
    - 1 terminal/linux node
    - 1 container test node 
    - 1 windows server 2022 as domain controller and internal DNS for Windows users. 
  - remote site 1
    - 1 pfsense fw setup as remote site 1
    - 1 iosvl2 switch
    - 1 windows 11 client
  - remote site 2
    - 1 fortigate 7.0 firewall
    - 1 iosvl2 switch
    - 1 Ubuntu 24.04 desktop client
  - remote site 3
    - 1 Cisco asa firewall
    - 1 iosvl2 switch
    - 1 Ubuntu 24.10 desktop client


The network diagram.







![image](src/images/main-topology-diagram.png "Lab Topology Diagram")

## Lab Instructions

- Configure spine-leaf
- Configure service leaf
- install proxmox on cluster 1
- install proxmox backup on pbs
- install truenas on nfs 1
- install proxmox on sandbox
- install and configure pfsense ha pair
- configure all fortios firewalls for standard outbound access
- configure fortinet ha pair to dc01
- configure dc01 fsmo roles
  - adds
  - dns
- configure active directory tst-ent.lan
  - domain user accounts
  - domain it admin
  - domain access across remote sites
- configure dcnm
  - implement fabric via mgmt network
- verify access to proxmox leaf 1
  - setup admin account
  - setup storage
  - setup iso repo
  - setup lxc containers
  - setup vm (test)
- verify access to proxmox pbs and truenas 
  - setup pbs backups
  - setup truenas nfs targets
    - cluster
    - sandbox


# to do 
  - implement ansible
    - integration
      - host
      - network appliance 
    - playbooks
      - ping playbooks
      - package deployment playbooks
      - network state
      - network changes
      
  - 



