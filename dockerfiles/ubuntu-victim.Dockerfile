FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    iproute2 \
    iputils-ping \
    net-tools \
    iptables \
    tcpdump \
    && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]