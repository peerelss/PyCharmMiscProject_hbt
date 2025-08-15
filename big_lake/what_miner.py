import os
import platform
import subprocess
import time
from whatsminer import WhatsminerAccessToken, WhatsminerAPI
import subprocess
import platform


def ping_ip(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    try:
        result = subprocess.run(
            ["ping", param, "1", ip],
            capture_output=True,
            text=True,
            timeout=3  # 可选，防止死等
        )
        output = result.stdout.lower()

        # Windows 返回 "reply from"
        # Linux/Mac 返回 "ttl="
        if "reply from" in output or "ttl=" in output:
            return True
        return False
    except Exception:
        return False


def check_ip_list(file_path):
    # 读取 IP 列表
    with open(file_path, 'r') as file:
        ips = [line.strip() for line in file if line.strip()]

    first_fail = []

    # 第一次 ping，记录失败的 IP
    print("🔍 第一次检测中...")
    for ip in ips:
        if not ping_ip(ip):
            first_fail.append(ip)

    # 稍作等待再试一次（可选）
    time.sleep(2)

    print("\n🔁 对第一次失败的 IP 再尝试一次...\n")

    truly_offline = []

    for ip in first_fail:
        if not ping_ip(ip):
            truly_offline.append(ip)

    # 输出真正离线的 IP
    print("❌ 以下 IP 连续两次 Ping 都失败，确认离线：\n")
    for ip in truly_offline:
        print(ip)


def get_miner_th_hash_by_ip(ip):
    try:
        token = WhatsminerAccessToken(ip_address=ip)
        summary_json = WhatsminerAPI.get_read_only_info(access_token=token,
                                                        cmd="get.device.info")
        return summary_json
    except Exception as e:
        return [ip, 0, str(e)]


import socket
import json
import struct

def miner_request(host, port, request_dict, timeout=5):
    """
    向矿机发送 JSON 请求并接收 JSON 响应
    host: 矿机 IP
    port: 矿机端口（协议说明是 4433）
    request_dict: 要发送的请求（Python 字典）
    timeout: socket 超时时间（秒）
    """
    # 1. 生成 JSON ASCII 数据
    json_str = json.dumps(request_dict, separators=(',', ':'))  # 去掉多余空格
    json_bytes = json_str.encode('ascii')

    # 2. 计算长度
    length = len(json_bytes)

    # 3. 连接矿机
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((host, port))

    try:
        # 4. 发送长度（4字节小端）
        sock.sendall(struct.pack('<I', length))  # <I = 小端 unsigned int (4字节)

        # 5. 发送 JSON 数据
        sock.sendall(json_bytes)

        # 6. 接收响应长度（4字节小端）
        len_bytes = sock.recv(4)
        if len(len_bytes) < 4:
            raise ValueError("未收到完整长度信息")
        resp_length = struct.unpack('<I', len_bytes)[0]

        # 7. 接收完整 JSON 响应
        resp_data = b''
        while len(resp_data) < resp_length:
            chunk = sock.recv(resp_length - len(resp_data))
            if not chunk:
                break
            resp_data += chunk

        # 8. 转成 Python 对象返回
        return json.loads(resp_data.decode('ascii'))

    finally:
        sock.close()




if __name__ == "__main__":
    # 示例请求
    host = "10.0.10.25"   # 矿机 IP
    port = 4433
    request = {
        "command": "get.device.info"  # 举例，实际看矿机 API
    }

    try:
        response = miner_request(host, port, request)
        print("矿机响应:", json.dumps(response, indent=2, ensure_ascii=False))
    except Exception as e:
        print("通信失败:", e)
