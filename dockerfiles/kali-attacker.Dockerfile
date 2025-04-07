FROM kalilinux/kali-rolling

RUN apt-get update && apt-get install -y \
    python3-scapy \
    net-tools \
    iputils-ping \
    tcpdump \
    && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]