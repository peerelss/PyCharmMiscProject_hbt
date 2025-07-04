import requests

from hbt_miner.fan_error import txt_2_list


def down_load_by_ip(ip):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': 'Digest username=root, realm=antMiner Configuration, nonce=fa6b40de72f629bdf89863f75ef56e46, uri=/cgi-bin/log.cgi, response=a3d89f8cb8e35c57db7e9ede98d41fea, qop=auth, nc=0000021f, cnonce=448a399aac2b1aa9',
        'Connection': 'keep-alive',
        'Referer': f'http://{ip}/',
        'Priority': 'u=0',
    }
    try:
        # 发送 GET 请求

        url = f"http://{ip}/log/antminer_log_2025-06-24_2025-07-04.tar"
        response = requests.get(f'http://{ip}/cgi-bin/dlog.cgi', headers=headers, timeout=5)
        print(response.content)
        response = requests.get(url, headers=headers, timeout=5)
        filename = f'antminer_log_2025-06-25_2025-07-04_{ip.replace(".", "_")}.tar'
        response.raise_for_status()  # 如果响应状态码不是 200，将引发 HTTPError

        with open(filename, 'wb') as f:
            f.write(response.content)

        print(f"文件已保存为：{filename}")

    except Exception as e:
        print(f"发生未知错误: {e}")
        return None


def create_log_by_ip(ip):

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="dafca33855faf10854d6ad92a68df523", uri="/cgi-bin/create_log_backup.cgi", response="0fa43501251215f4eda8eba6fd631170", qop=auth, nc=00000033, cnonce="488ae077db3814ff"',
        'Connection': 'keep-alive',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'http://10.82.1.1',
        'Referer': 'http://10.82.1.1/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = '["/2025-06/25","/2025-06/26","/2025-06/27","/2025-06/28","/2025-06/29","/2025-06/30","/2025-07/01","/2025-07/02","/2025-07/03","/2025-07/04"]'

    response = requests.post(f'http://{ip}/cgi-bin/create_log_backup.cgi', headers=headers, data=data, verify=False)
    print(response.content)


if __name__ == '__main__':
    ips = txt_2_list('fans.txt')
    for ip in ips:
        # print(ip)
        create_log_by_ip(ip)
        down_load_by_ip(ip)
