FROM debian:stretch-slim

MAINTAINER Khelil Sator <ksator@juniper.net>

RUN apt-get update && \ 
    apt-get install -y --no-install-recommends wget python-pip nano vim tcpdump gnupg2 iputils-ping && \ 
    wget -O - https://repo.saltstack.com/apt/debian/9/amd64/archive/2018.3.2/SALTSTACK-GPG-KEY.pub | apt-key add - && \
    echo 'deb http://repo.saltstack.com/apt/debian/9/amd64/archive/2018.3.2 stretch main' > /etc/apt/sources.list.d/saltstack.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends salt-minion && \
    apt-get remove -y wget
    #apt-get --auto-remove --yes remove python-openssl

RUN pip install --upgrade setuptools
RUN pip install wheel && \
    pip install pyOpenSSL junos-eznc jxmlease jsnapy && \
    rm -rf /var/lib/apt/lists/*

#COPY minion /etc/salt/minion
#COPY proxy /etc/salt/proxy

ENTRYPOINT service salt-minion start && bash
