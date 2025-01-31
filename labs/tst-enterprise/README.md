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


## The network diagram.







![image](src/images/main-topology-diagram.png "Lab Topology Diagram")

## Lab Instructions

- Configure spine-leaf
- Configure service leaf
- Install proxmox on cluster 1
- Install proxmox backup on pbs
- Install truenas on nfs 1
- Install proxmox on sandbox
- Install and configure pfsense ha pair
- Configure all fortios firewalls for standard outbound access
- Configure fortinet ha pair to dc01
- Configure dc01 fsmo roles
  - ADDS
  - DNS
- Configure active directory tst-ent.lan
  - Domain user accounts
  - Domain it admin
  - Domain access across remote sites
- Configure dcnm
  - Implement fabric via mgmt network
- Verify access to proxmox leaf 1
  - Setup admin account
  - Setup storage
  - Setup iso repo
  - Setup lxc containers
  - Setup vm (test)
- verify access to proxmox pbs and truenas 
  - Setup pbs backups
  - Setup truenas nfs targets
    - Cluster
    - Sandbox


# to do 
  - Implement Ansible
    - Integration
      - Host
      - Network appliance 
    - playbooks
      - Ping
      - Package deployment playbooks
      - Network state
      - Network changes


