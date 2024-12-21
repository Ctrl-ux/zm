from scapy.all import *
from pymodbus.client.sync import ModbusTcpClient
import os
import time
import threading
import struct
import binascii
from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import ARP, getmacbyip, Ether





def disable_ip_forwarding():
    """禁用 IP 转发"""
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
        f.write('0')



def packet_callback(packet):
    """捕获流量并处理 Modbus TCP 流量"""
    try:
        if packet.haslayer(Ether):
            # 获取目的 MAC 地址
            dst_mac = packet[Ether].dst

            # 过滤条件：如果目的 MAC 地址是本机的 MAC 地址，则处理数据包
            my_mac = get_if_hwaddr(conf.iface)  # 获取本机的 MAC 地址
            if dst_mac == my_mac:
                print(f"[INFO] 捕获到目的 MAC 地址是我的数据包: {binascii.hexlify(bytes(packet)).decode()}")
                # 在这里可以添加其他处理数据包的代码
            else:
                print(f"[INFO] 捕获到目的 MAC 地址不是我的，跳过此包")
                return
        else:
            print("[INFO] 捕获的不是以太网数据包")

        # 检查数据包是否为 IP 包
        if packet.haslayer(IP):
            # 提取 IP 层
            ip = packet[IP]
            print(f"[INFO] 捕获到 IP 数据包:")
            print(f"源 IP: {ip.src}, 目标 IP: {ip.dst}")
            print(f"IP 数据包 (16 进制): {binascii.hexlify(bytes(ip)).decode()}")

            # 提取 IP 数据包的负载部分并打印 16 进制
            ip_data = bytes(ip.payload)
            print(f"IP 数据负载 (16 进制): {binascii.hexlify(ip_data).decode()}")

            # 检查是否包含 TCP 层
            if packet.haslayer(TCP):
                # 提取 TCP 层
                tcp = packet[TCP]
                print(f"[INFO] 捕获到 TCP 数据包:")
                print(f"源端口: {tcp.sport}, 目标端口: {tcp.dport}")
                print(f"TCP 头部 (16 进制): {binascii.hexlify(bytes(tcp)).decode()}")

                # 检查 TCP 数据部分是否为空
                if len(tcp.payload) > 0:
                    print(f"TCP 数据部分 (16 进制): {binascii.hexlify(bytes(tcp.payload)).decode()}")

                    # 如果 TCP 数据部分不为空，组合新的 IP 和 TCP 数据包
                    new_tcp = TCP(sport=tcp.sport, dport=tcp.dport, seq=tcp.seq, ack=tcp.ack, flags=tcp.flags,
                                  window=tcp.window, chksum=None)  # 复制 TCP 头部

                    # 输出新的 IP 数据包的 16 进制
                    if ip.src == "192.168.103.140":
                        target_mac = getmacbyip("10.0.0.1")  # 获取 10.0.0.138 的 MAC 地址
                        new_ip = IP(src="10.0.0.138", dst="10.2.0.199")  # 新的 IP 数据包
                        # 组合新的 IP 数据包和 TCP 数据包
                        new_ip = new_ip / new_tcp / tcp.payload
                    elif ip.src == "10.2.0.199":
                        target_mac = getmacbyip("192.168.103.140")  # 获取 10.0.0.138 的 MAC 地址
                        new_ip = IP(src="10.0.0.138", dst="192.168.103.140")  # 新的 IP 数据包
                        # 组合新的 IP 数据包和 TCP 数据包
                        new_ip = new_ip / new_tcp / tcp.payload
                    else:
                        target_mac = getmacbyip(ip.dst)  # 默认获取 ip.dst 的 MAC 地址
                    # 获取目标 MAC 地址
                    if target_mac:
                        print(f"[INFO] 目标 MAC 地址: {target_mac}")
                        # 获取网络接口并发送新的数据包
                        iface = conf.iface  # 自动选择网络接口
                        sendp(Ether(dst=target_mac) / new_ip, iface=iface, verbose=False)
                        print(f"[INFO] 转发数据包到目标 MAC: {target_mac}")
                    else:
                        print(f"[ERROR] 无法获取目标 IP ({ip.dst}) 的 MAC 地址")
                else:
                    # 如果 TCP 数据部分为空，直接使用现有的 IP 和 TCP 数据包
                    print("[INFO] TCP 数据部分为空，可能是控制包，直接发送原始包")
                    # 如果 TCP 数据部分不为空，组合新的 IP 和 TCP 数据包
                    new_tcp = TCP(sport=tcp.sport, dport=tcp.dport, seq=tcp.seq, ack=tcp.ack, flags=tcp.flags,
                                  window=tcp.window, chksum=None)  # 复制 TCP 头部

                    # 输出新的 IP 数据包的 16 进制
                    if ip.src == "192.168.103.140":
                        target_mac = getmacbyip("10.0.0.1")  # 获取 10.0.0.138 的 MAC 地址
                        new_ip = IP(src="10.0.0.138", dst="10.2.0.199")  # 新的 IP 数据包
                        # 组合新的 IP 数据包和 TCP 数据包
                        new_ip = new_ip / new_tcp / tcp.payload
                    elif ip.src == "10.2.0.199":
                        target_mac = getmacbyip("192.168.103.140")  # 获取 10.0.0.138 的 MAC 地址
                        new_ip = IP(src="10.0.0.138", dst="192.168.103.140")  # 新的 IP 数据包
                        # 组合新的 IP 数据包和 TCP 数据包
                        new_ip = new_ip / new_tcp / tcp.payload
                    else:
                        target_mac = getmacbyip(ip.dst)  # 默认获取 ip.dst 的 MAC 地址
                    # 获取目标 MAC 地址
                    if target_mac:
                        print(f"[INFO] 目标 MAC 地址: {target_mac}")
                        # 获取网络接口并发送新的数据包
                        iface = conf.iface  # 自动选择网络接口
                        sendp(Ether(dst=target_mac) / new_ip, iface=iface, verbose=False)
                        print(f"[INFO] 转发数据包到目标 MAC: {target_mac}")
                    else:
                        print(f"[ERROR] 无法获取目标 IP ({ip.dst}) 的 MAC 地址")
            else:
                print("[INFO] 捕获的不是 TCP 数据包")
        else:
            print("[INFO] 捕获的不是 IP 数据包")

    except Exception as e:
        print(f"[ERROR] 处理包时出错: {e}")


def main():

    # 自动选择活动接口
    iface = conf.iface  # 使用 Scapy 自动选择活动的网络接口

    if iface is None:
        print("[ERROR] 未找到有效的网络接口")
        return

    # 获取 MAC 地址
    attacker_mac = get_if_hwaddr(iface)  # 本机 MAC 地址

    print(f"[INFO]  MAC: {attacker_mac}")

    # 启动一个线程捕获目标设备和网关之间的 Modbus TCP 流量
    filter = f"ether dst {attacker_mac} and tcp port 502"
    capture_thread = threading.Thread(
        target=lambda: sniff(iface=iface, filter=filter, prn=packet_callback, store=False))
    capture_thread.daemon = True  # 设置为守护线程，这样主线程退出时它也会自动结束
    capture_thread.start()



if __name__ == "__main__":
    main()