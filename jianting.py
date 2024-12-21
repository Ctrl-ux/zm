from scapy.all import *

def packet_callback(packet):
    """捕获 TCP 流量并打印详细信息，包括序列号和确认号"""
    # 仅处理具有 IP 和 TCP 层的数据包
    if packet.haslayer(IP) and packet.haslayer(TCP):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        tcp_sport = packet[TCP].sport
        tcp_dport = packet[TCP].dport
        tcp_seq = packet[TCP].seq
        tcp_ack = packet[TCP].ack
        tcp_flags = packet[TCP].flags

        # 打印捕获到的 TCP 包的详细信息
        print(f"[INFO] 捕获到 TCP shujubao: {ip_src} -> {ip_dst} | TCP {tcp_sport} -> {tcp_dport}")
        print(f"       xuliehao: {tcp_seq}, queren: {tcp_ack}, TCP 标志: {tcp_flags}")

# 设置网卡接口，这里假设网卡名为 'ens33'，你可以根据你的系统修改
interface = "eth0"

# 启动数据包捕获，过滤条件为所有的 TCP 数据包
print("[INFO] 正在捕获 TCP 数据包...")
sniff(iface=interface, filter="tcp", prn=packet_callback, store=0)
