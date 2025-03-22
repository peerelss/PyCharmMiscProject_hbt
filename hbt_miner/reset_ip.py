import requests
import json


def set_antminer_ip(miner_ip, new_ip, gateway, subnet="255.255.255.0", dns="8.8.8.8"):
    url = f"http://{miner_ip}/cgi-bin/set_network_conf.cgi"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://10.21.1.143',
        'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="9fa8e80f9182ac436829fc33db0de474", uri="/cgi-bin/set_network_conf.cgi", response="b1895bc469c0b5d9c07ef0b31b6624dc", qop=auth, nc=0000007b, cnonce="9377182559e500e8"',
        'Connection': 'keep-alive',
        'Referer': 'http://10.21.1.143/',
        'Priority': 'u=0',
        "Content-Type": "application/json",  # 这里要用 `application/json`
    }

    # 构造请求数据
    payload = {
        'ipHost': "Antminer",
        'ipPro': 2,
        'ipAddress': new_ip,
        'ipSub': '255.255.240.0',
        'ipGateway': '10.21.1.254',
        'ipDns': "8.8.8.8",
    }

    # 发送请求
    response = requests.post(url, data=payload, headers=headers)
    print(payload)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"修改失败，状态码: {response.status_code}, 响应: {response.text}")


# 示例调用
miner_ip = "10.21.11.143"  # 矿机当前IP
new_ip = "10.21.1.143"  # 目标新IP
gateway = "10.21.1.254"  # 计算的网关地址

set_antminer_ip(miner_ip, new_ip, gateway)
