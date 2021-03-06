# About this project

This repository provides Dockerfiles for SaltStack master and minion, including the dependencies to use Junos modules and Junos syslog engine.  
It has also a script that generate SaltStack files (minion and proxy configuration files, pillars ....)  
This repository has been tested with an Ubuntu host running 16.04 release.  

# How to use this repository

## Requirements to use this repository

You first need to install some requirements on your Ubuntu host 

### Install these dependencies 

```
sudo apt-get update
sudo apt-get install python-pip -y
pip install pyyaml jinja2
pip list
``` 

### Install docker 

Check if Docker is already installed 
```
$ docker --version
```

If it was not already installed, install it. Here's how to install in on Ubuntu 16.04:  
```
$ sudo apt-get update
```
```
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```
```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
```
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```
```
$ sudo apt-get update
```
```
$ sudo apt-get install -y docker-ce docker-compose
```
```
$ sudo docker run hello-world
```
```
$ sudo groupadd docker
```
```
$ sudo usermod -aG docker $USER
```

Exit the ssh session to your ubuntu and open an new ssh session to your ubuntu and run these commands to verify you installed Docker properly:  
```
$ docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/
```
```
$ docker --version
Docker version 18.03.1-ce, build 9ee9f40
```

## Clone the repository
```
git clone https://github.com/ksator/saltstack-junos-docker.git
cd saltstack-junos-docker
```

## Create a docker image for the master
It will include the Junos syslog engine dependencies 
```
cd master
sudo docker build -t saltmaster-junossyslog .
```
Verify
```
docker images
```


## Create a docker image for the minion
It will include the junos modules dependencies
```
cd ../minion
sudo docker build -t saltminion-junosproxy .
```
Verify
```
docker images
```
## Instantiate a master and minion containers
```
docker-compose up -d
```

## How to connect to a container cli? 
Connect to a master container cli and run these commands: 
```
docker exec -it master bash

```
## Update the variables 
```
vi /srv/templates/variables.yml
```
## Run this script 
It will use your variables to create saltstack files (pillars, minion and proxy configurartion files, ...) 

```
python render.py
```
Connect to a minion container cli if needed: 
```
docker exec -it minion1 bash
exit
```

## Verify the setup works
```
docker exec -it master salt-key -L
```
```
docker exec -it master salt minion1 test.ping
docker exec -it master salt "minion1" cmd.run "pwd"
```
```
docker exec -it minion1 salt-proxy -d --proxyid=dc-vmx-3
docker exec -it master salt dc-vmx-3 junos.cli 'show chassis hardware'
```

## Verify the junos syslog engine 
```
docker exec -it master salt 'dc-vmx-3' state.apply syslog
```
Connect to the master cli and watch the event bus:  
```
docker exec -it master bash
salt-run state.event pretty=True
```
ssh the junos device and commit a configuration change and watch the event bus on the master
