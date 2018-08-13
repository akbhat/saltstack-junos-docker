FROM debian:stretch-slim

MAINTAINER Khelil Sator <ksator@juniper.net> 

RUN apt-get update && \
    apt-get install -y --no-install-recommends wget nano vim tcpdump python-pip gnupg2 iputils-ping && \
    wget -O - https://repo.saltstack.com/apt/debian/9/amd64/archive/2018.3.2/SALTSTACK-GPG-KEY.pub | apt-key add - && \
    echo 'deb http://repo.saltstack.com/apt/debian/9/amd64/archive/2018.3.2 stretch main' > /etc/apt/sources.list.d/saltstack.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends salt-master salt-minion salt-cloud && \
    apt-get remove -y wget
    
RUN pip install --upgrade setuptools
RUN pip install wheel && \
    pip install pyOpenSSL junos-eznc jxmlease jsnapy && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /srv/pillar /srv/salt
COPY master /etc/salt/master
COPY templates /srv/templates
COPY syslog.sls /srv/salt/syslog.sls

#https://github.com/saltstack/salt/pull/46804
# Add Tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

CMD service salt-master start && service salt-minion start && bash
