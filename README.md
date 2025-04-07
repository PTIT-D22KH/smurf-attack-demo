
# Cách chạy container

## Chạy file docker-compose.yml

```bash
docker-compose up
```

## Demo tấn công:
### Terminal 1 - Nạn nhân
```bash
docker exec -it vuln-victim tcpdump -i eth0 icmp
```
###  Terminal 2 - Khuếch đại
```bash
docker exec -it vuln-amplifier tcpdump -i eth0 icmp
```

### Terminal 3 - Tấn công
```bash
docker exec -it vuln-attacker bash
cd /attack_scripts
python3 smurf_attack.py 172.20.0.2 172.20.255.255
```
hoặc

```bash
docker exec -it vuln-attacker bash -c "cd /attack_scripts && python3 smurf_attack.py 172.20.0.2 172.20.255.255"
```

## Demo phòng thủ:
### Terminal nạn nhân
```bash
docker exec -it prot-victim tcpdump -i eth0 icmp
```
### Terminal khuếch đại
```bash
docker exec -it prot-amplifier tcpdump -i eth0 icmp
```
### Terminal kẻ tấn công
```bash
docker exec -it prot-attacker bash
cd /attack_scripts
python3 smurf_attack.py 172.21.0.2 172.21.255.255
```
hoặc
```bash
docker exec -it prot-attacker bash -c "cd /attack_scripts && python3 smurf_attack.py 172.21.0.2 172.21.255.255"
```
