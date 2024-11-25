from scapy.all import getmacbyip

# 替换为目标设备和网关的 IP 地址
target_ip = "10.2.0.195"
gateway_ip = "10.2.0.1"

# 获取 MAC 地址
target_mac = getmacbyip(target_ip)
gateway_mac = getmacbyip(gateway_ip)

# 输出结果
print(f"{target_mac}")
print(f"{gateway_mac}")
