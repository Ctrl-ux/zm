from pymodbus.client.sync import ModbusTcpClient
import time

def create_modbus_request(server_ip, unit_id=1):
    """创建一个 Modbus TCP 请求包并连接 Modbus 服务器"""
    # 创建一个 Modbus 客户端连接，连接到目标 Modbus 服务器
    client = ModbusTcpClient(server_ip, port=502, timeout=5)  # 设置更长的超时
    if not client.connect():
        print("[ERROR] 无法连接到 Modbus 服务器")
        return None

    # 向服务器请求 10 个离散输入（功能码 2）
    try:
        result = client.read_holding_registers(0, 9)
        if result.isError():
            print(f"[ERROR] Modbus 请求失败: {result}")
        else:
            print(f"[INFO] 接收到的 Modbus 响应: ")
            print(result.registers)
    except Exception as e:
        print(f"[ERROR] 请求发送失败: {e}")
    finally:
        client.close()


def main():
    """目标主机持续发送 Modbus TCP 报文"""
    unit_id = 1  # 假设设备的 Modbus 单元 ID 为 1
    server_ip = '192.168.88.138'  # 假设 Modbus 服务器（攻击主机）的 IP 地址
    while True:
        print("[INFO] 发送 Modbus 请求 ...")
        create_modbus_request(server_ip, unit_id)
        time.sleep(2)  # 每 2 秒发送一次请求

if __name__ == "__main__":
    main()
