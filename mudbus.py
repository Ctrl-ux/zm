import logging
from pymodbus.server.sync import ModbusTcpServer
from pymodbus.datastore import ModbusSparseDataBlock
from pymodbus.device import ModbusDeviceIdentification

logging.basicConfig(level=logging.DEBUG)

print("pymodbus 模块导入成功")

def run_modbus_server():
    """运行一个 Modbus TCP 服务器并响应客户端请求"""
    store = ModbusSparseDataBlock({0: 0x01, 1: 0x02, 2: 0x03, 3: 0x04})

    print("数据块创建成功")

    server = ModbusTcpServer(store, address=("0.0.0.0", 502))

    print("Modbus 服务器创建成功")

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Test Vendor'
    identity.ProductCode = 'Modbus TCP'
    server.server_identification = identity

    print("Modbus 设备信息设置成功")

    print("[INFO] Modbus 服务器已启动...")
    server.serve_forever()

if __name__ == "__main__":
    run_modbus_server()
