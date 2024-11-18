## TST Netboot Lab

  - Lab to provision pxe solution for enterprise. 
  - Lab instructions
    1. Configure tst-lab-fw-01 port1 as WAN, port2 as LAN
      - Configure DHCP for LAN for PXE boot poiting to netboot server. 
    2. Configure netboot server - Ubuntu 22.04 / docker / netboot.xyz container
      - Configure local assets for Ubuntu 24.04 / 22.04 / Kali Linux / Windows 11
    3. Configure ansible server - Ubuntu 22.04 / ansible / docker
    4. Configure orchestrator (sysadmin) - vscode / powershell 7.4.6 or later
      - Use VSCode to interact with ansible
      - Configure ping / get facts playbooks against network infrastructure
      - Configure node mgmt / ping / get facts / update / add packages
    5. Configure 3 empty vms for uefi boot. 



## Lab Diagram 





![image](src/images/main-topology-diagram.png "Lab Topology Diagram")