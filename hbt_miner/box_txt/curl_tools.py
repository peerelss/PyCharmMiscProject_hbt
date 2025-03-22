import requests


def change_miner_ip(old_ip, new_ip):
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

    data = {
        "ipHost": "Antminer",
        "ipPro": 2,
        "ipAddress": new_ip,
        "ipSub": "255.255.240.0",
        "ipGateway": "10.21.1.254",
        "ipDns": "8.8.8.8",
    }

    response = requests.post(url, headers=headers, json=data)

    # 输出响应结果
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)


if __name__ == '__main__':
    change_miner_ip('10.21.1.143', '10.21.11.143')
