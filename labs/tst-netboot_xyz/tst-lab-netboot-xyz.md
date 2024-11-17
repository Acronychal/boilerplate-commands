# netboot

```
#install docker
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

#create netboot docker environment
mkdir netboot
cd netboot
mkdir assets config
touch docker_compose.yml


```
edit docker_compose.yml
```
nano docker_compose.yml
---
version: "2.1"
services:
  netbootxyz:
    image: lscr.io/linuxserver/netbootxyz:latest
    container_name: netbootxyz
    environment:
      - PUID=1000 #current user
      - PGID=1000 #current group
      - TZ=Etc/UTC
      # - MENU_VERSION=1.9.9 #optional, sets menus version, unset uses latest
      - PORT_RANGE=30000:30010 #optional
      - SUBFOLDER=/ #optional
    volumes:
      - ./config:/config
      - ./assets:/assets #optional
    ports:
      - 3000:3000
      - 69:69/udp
      - 8080:80 #optional
    restart: unless-stopped
```
run the container
```
docker compose up -d
docker ps



