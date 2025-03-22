import requests
import os
import subprocess
import platform

def change_miner_ip(old_ip, new_ip):
    if is_ip_online(new_ip):
        print(f'{new_ip}ip重复')
        return
    url = f"http://{old_ip}/cgi-bin/set_network_conf.cgi"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "http://10.21.1.143",
        "Authorization": 'Digest username="root", realm="antMiner Configuration", nonce="9fa8e80f9182ac436829fc33db0de474", uri="/cgi-bin/set_network_conf.cgi", response="b449a3d07af344ac4e9648a20432d55d", qop=auth, nc=00000112, cnonce="2a89380be3b430b5"',
        "Connection": "keep-alive",
        "Referer": "http://10.21.1.143/",
        "Priority": "u=0",
    }
    parts = old_ip.split('.')
    gateway = "10.21.1.254"
    # 确保 IP 地址格式正确
    if len(parts) != 4:
        raise ValueError("无效的 IP 地址格式")
    else:
        # 提取前两位并生成网关地址
        gateway = f"{parts[0]}.{parts[1]}.1.254"
    data = {
        "ipHost": "Antminer",
        "ipPro": 2,
        "ipAddress": new_ip,
        "ipSub": "255.255.240.0",
        "ipGateway": gateway,
        "ipDns": "8.8.8.8",
    }
    try:
        response = requests.post(url, headers=headers, json=data)

        # 输出响应结果
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
        if response.json()['stats'] == 'success':
            print(f"修改{old_ip}成功")
        else:
            print(f"修改{old_ip}发生错误  ")
    except Exception as e:
        print(f"修改{old_ip}发生未知错误: {e}")


def is_ip_online(ip):
    # 根据系统选择 ping 命令
    if platform.system().lower() == "windows":
        cmd = ["ping", "-n", "1", "-w", "1000", ip]  # Windows
    else:
        cmd = ["ping", "-c", "1", "-W", "1", ip]  # Linux/macOS

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0  # returncode == 0 表示成功
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == '__main__':
    #  change_miner_ip('10.21.1.143', '10.21.11.143')
    ip_address = "10.21.1.143"
    if is_ip_online(ip_address):
        print(f"{ip_address} 在线")
    else:
        print(f"{ip_address} 不在线")
