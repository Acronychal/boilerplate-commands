# NS-OSv Basic Info
- Configure password for admin after boot. 
    ```
    configure terminal
    hostname <name>

- enable features ospf
    ```
    feature ospf
    router ospf 1
    router-id <x.x.x.x>
    network 0.0.0.0 0.0.0.0 area 0
    exit
    configure terminal
    interface <interface>
    ip router ospf 1 area 0
    


