import socket
import threading

# 目标IP和端口
target_ip = '10.4.3.195'  # 替换为实际的目标IP
target_port = 4840  # 替换为实际的目标端口

def test_connection(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)  # 设置超时时间为5秒
        s.connect((ip, port))
        print(f"Successfully connected to {ip}:{port}")
        s.close()
    except ConnectionRefusedError:
        print(f"Connection to {ip}:{port} refused")
    except Exception as e:
        print(f"An error occurred: {e}")

# 进行单次连接测试
test_connection(target_ip, target_port)

def test_connection_thread(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)  # 设置超时时间为5秒
        s.connect((ip, port))
        print(f"Successfully connected to {ip}:{port}")
        s.close()
    except ConnectionRefusedError:
        print(f"Connection to {ip}:{port} refused")
    except Exception as e:
        print(f"An error occurred: {e}")

# 创建多个线程进行测试
threads = []
num_threads = 50  # 你可以调整线程的数量
for i in range(num_threads):
    thread = threading.Thread(target=test_connection_thread, args=(target_ip, target_port))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()
