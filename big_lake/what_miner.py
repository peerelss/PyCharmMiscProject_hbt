import os
import platform
import subprocess
import time

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


if __name__ == "__main__":
    check_ip_list("ip_list.txt")
# print(ping_ip("10.0.10.80"))
