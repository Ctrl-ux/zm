from pymodbus.server.sync import ModbusTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import logging

logging.basicConfig(level=logging.DEBUG)

def run_modbus_server():
    """运行一个 Modbus TCP 服务器并响应客户端请求"""
    # 创建一个数据块，包含更多寄存器
    store = ModbusSequentialDataBlock(0, [0x00] * 10)  # 初始化10个寄存器，每个寄存器的值为 0x00
    # 创建一个 ModbusSlaveContext，将数据块与 Modbus 设备关联
    slave_context = ModbusSlaveContext(hr=store)  # hr 表示保持寄存器（Holding Registers）
    context = ModbusServerContext(slaves=slave_context, single=True)  # 创建 Modbus 服务器上下文

    print("数据块创建成功")

    # 创建 Modbus 服务器并启动
    server = ModbusTcpServer(context, address=("0.0.0.0", 502))

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
