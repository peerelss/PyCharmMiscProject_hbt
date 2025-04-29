import time
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import pandas as pd
import os
import csv
import concurrent.futures
import asyncio
import aiohttp

from hbt_miner.miner_online_ip import generate_ip_list

box_list = ['11', '12', '21', '22', '31', '32', '41', '42', '51', '52', '61', '62', '71', '72', '81', '82', '91', '92',
            '101', '102']
import subprocess
import platform


# txt 2 list
def txt_2_list(txt_path):
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()  # 每行作为列表元素
            lines = [line.strip() for line in lines]  # 去掉换行符
        return lines
    except Exception as e:
        print(f"读取 Excel 文件时出错: {e}")
        return []


def csv_2_list(csv_path):
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8', errors="ignore") as file:
            reader = csv.reader(file)
            # 跳过第一行（标题行）
            next(reader)
            data = [row for row in reader]  # 转换为二维数组
            return data
    else:
        print(f'{csv_path}   not exist')
        return []


def get_sn_from_ip(ip):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': 'Digest username=root, realm=antMiner Configuration, nonce=571e8735e2cee0138dc43d18fc989641, uri=/cgi-bin/get_system_info.cgi, response=8de0922b966f7025b548010935990c7b, qop=auth, nc=0000053a, cnonce=71310d5e384a4188',
        'Connection': 'keep-alive',
        'Referer': 'http://10.11.1.11/',
    }
    try:
        response = requests.get(f'http://{ip}/cgi-bin/get_system_info.cgi', headers=headers)
        sn = response.json()['serinum']
        #  print(f"{ip} sn:  {sn}")
        return sn
    except Exception as e:
        print(f"{ip}发生未知错误: {e}")
        return ''


def update_firmware_by_ip(ip, path):
    url = "http://10.62.1.96/cgi-bin/upgrade.cgi"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "multipart/form-data; boundary=----geckoformboundaryad7db04024595aea268025b3a5a12e24",
        "Origin": "http://10.62.1.96",
        "Authorization": "Digest username=\"root\", realm=\"antMiner Configuration\", nonce=\"0bf55f31cd8ddd7c45a38eabc0e23968\", uri=\"/cgi-bin/upgrade.cgi\", response=\"8b6107828273e26c682dcbc38de6da4e\", qop=auth, nc=00000049, cnonce=\"f5de0598512518d8\"",
        "Connection": "keep-alive",
        "Referer": "http://10.62.1.96/"
    }

    # multipart form boundary data
    payload = "------geckoformboundaryad7db04024595aea268025b3a5a12e24"

    response = requests.post(url, headers=headers, data=payload)

    print(response.status_code)
    print(response.text)


# data 2 excel
def data_2_excel(data_result):
    df = pd.DataFrame(data_result)
    # 保存为 Excel 文件
    time_now = datetime.now().strftime("%Y-%m-%d%H_%M_%S")
    df.to_excel(f"output__{time_now}.xlsx", index=False, header=False)
    print("Excel 文件已生成：output.xlsx")


def is_ip_online(ip):
    # 根据系统选择 ping 命令
    if platform.system().lower() == "windows":
        cmd = ["ping", "-n", "1", "-w", "1000", ip]  # Windows
    else:
        cmd = ["ping", "-c", "1", "-W", "1", ip]  # Linux/macOS

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0  # return code == 0 表示成功
    except Exception as e:
        print(f"Error: {e}")
        return False


def count_online_ips(ip_range):
    start_ip, end_ip = ip_range.split("-")
    base_ip = ".".join(start_ip.split(".")[:-1])  # 提取前 3 段 IP
    start_num = int(start_ip.split(".")[-1])
    end_num = int(end_ip.split(".")[-1])
    online_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        ip_list = [f"{base_ip}.{i}" for i in range(start_num, end_num + 1)]
        results = executor.map(is_ip_online, ip_list)

    online_count = sum(results)
    return online_count


def count_box(box_no):
    return count_online_ips(f'10.{box_no}.1.1-10.{box_no}.1.168') + count_online_ips(
        f'10.{box_no}.2.1-10.{box_no}.2.168')


def multi_task(fun_foo, data_bar):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(fun_foo, data_bar))

    return results


def light_miner(ip):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'http://10.92.1.20',
        'Authorization': 'Digest username=root, realm=antMiner Configuration, nonce=3b3d7ff74ce6f091386af3a9be81347e, uri=/cgi-bin/blink.cgi, response=5d08897e698594246adf59f13dcc701a, qop=auth, nc=0000003b, cnonce=b320d281e94e1c5a',
        'Connection': 'keep-alive',
        'Referer': 'http://10.92.1.20/',
        'Priority': 'u=0',
    }

    data = '{blink:true}'
    try:

        response = requests.post(f'http://{ip}/cgi-bin/blink.cgi', headers=headers, data=data)
        print(f'{ip}')
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return ""


def set_miner_work_miner(ip):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'http://10.41.10.2',
        'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="8af871024deba26e9098078766341bd2", uri="/cgi-bin/set_miner_conf.cgi", response="d786134c7b5daf0ea46dd57f843e9d73", qop=auth, nc=00000072, cnonce="cb1bd2f87127965a"',
        'Connection': 'keep-alive',
        'Referer': 'http://10.41.10.2/',
        'Priority': 'u=0',
    }

    data = '{"bitmain-fan-ctrl":false,"bitmain-fan-pwm":"100","bitmain-hashrate-percent":"100","miner-mode":0,"freq-level":"100","pools":[{"url":"stratum+tcp://ss.antpool.com:3333","user":"AMTX22.10x41x10x230","pass":"root"},{"url":"stratum+tcp://ss.antpool.com:443","user":"AMTX22.10x41x10x230","pass":"root"},{"url":"stratum+tcp://btc.f2pool.com:1314","user":"amtx22f2pool.10x41x10x230","pass":"root"}]}'
    try:
        response = requests.post(f'http://{ip}/cgi-bin/set_miner_conf.cgi', headers=headers, data=data)
        print(ip, response.json())
    except Exception as e:
        print(f"Error: {e}")
        return ""


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate',
    'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="517d6873129c6f9123f476c4bd84283d", uri="/cgi-bin/get_system_info.cgi", response="45782a78f62e6e6934cb5405da972164", qop=auth, nc=00000002, cnonce="b77e46ff962779da"',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Priority': 'u=0, i',
}


async def get_system_info(ip, session):
    try:
        async with session.get(f'http://{ip}/cgi-bin/summary.cgi', headers=headers, timeout=2) as res_json:
            json_data = await res_json.json(content_type=None)
            return ip, json_data

    except Exception as e:
        return ip, str(e)


async def run_get_info():
    start_time = time.time()  # <-- 记录开始时间
    ips = txt_2_list('fans.txt')
    async with aiohttp.ClientSession() as session:
        tasks = [get_system_info(ip, session) for ip in ips]
        results = await asyncio.gather(*tasks)
        print(results)
    end_time = time.time()  # <-- 记录结束时间
    print(f"\n⏱️ 扫描耗时: {end_time - start_time:.2f} 秒")


def get_status(ip):
    try:
        response = requests.get('http://10.11.1.1/cgi-bin/get_system_info.cgi', headers=headers)
        print(ip, response.json())
    except Exception as e:
        return ip, str(e)


def run_normal_task():
    start_time = time.time()  # <-- 记录开始时间
    ips = txt_2_list('fans.txt')
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(get_status, ips))
    end_time = time.time()  # <-- 记录结束时间
    print(f"\n⏱️ 扫描耗时: {end_time - start_time:.2f} 秒")


def get_miner_net_config(ip):
    try:
        response = requests.get(f'http://{ip}/cgi-bin/get_network_info.cgi', headers=headers)
        net_gateway = response.json()['conf_gateway']
        if str(net_gateway).endswith('2.254'):
            print(ip, net_gateway)
        return ip, response.json()['conf_gateway']

    except Exception as e:
        return ip, str(e)


def change_work_mode(ip):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'http://10.102.1.143',
        'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="68695f7e82979e8636957c0788c7cb19", uri="/cgi-bin/set_miner_conf.cgi", response="a954bf4eff410b6eb0ffb26f4a866c66", qop=auth, nc=00000041, cnonce="0664436edfd7834f"',
        'Connection': 'keep-alive',
        'Referer': 'http://10.102.1.143/',
        'Priority': 'u=0',
    }

    data = '{"bitmain-fan-ctrl":false,"bitmain-fan-pwm":"100","bitmain-hashrate-percent":"100","miner-mode":0,"freq-level":"100","pools":[{"url":"stratum+tcp://ss.antpool.com:3333","user":"AMTX22.10x41x10x230","pass":"root"},{"url":"stratum+tcp://ss.antpool.com:443","user":"AMTX22.10x41x10x230","pass":"root"},{"url":"stratum+tcp://btc.f2pool.com:1314","user":"amtx22f2pool.10x41x10x230","pass":"root"}]}'

    try:
        response = requests.post(f'http://{ip}/cgi-bin/set_miner_conf.cgi', headers=headers, data=data)
        print(ip, response.json())
        return ip

    except Exception as e:
        return ip, str(e)


async def run_change_work_mode():
    start_time = time.time()  # <-- 记录开始时间
    ips = txt_2_list('fans.txt')
    async with aiohttp.ClientSession() as session:
        tasks = [change_work_mode(ip, session) for ip in ips]
        results = await asyncio.gather(*tasks)
        print(results)
    end_time = time.time()  # <-- 记录结束时间
    print(f"\n⏱️ 扫描耗时: {end_time - start_time:.2f} 秒")


def get_miner_net_config_by_box(box_id):
    ip_list = []

    # 第一段：10.box_id.1.1 ~ 10.box_id.1.168
    for i in range(1, 169):
        ip_list.append(f"10.{box_id}.1.{i}")

    # 第二段：10.box_id.2.1 ~ 10.box_id.2.168
    for i in range(1, 169):
        ip_list.append(f"10.{box_id}.2.{i}")

    return ip_list


def work_mode():
    # asyncio.run(run_change_work_mode())
    ips = txt_2_list('fans.txt')
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(change_work_mode, ips))


def get_all_offline():
    offline_ip = []
    for box in box_list:
        ips = get_miner_net_config_by_box(box)
        for ip in ips:
            if not is_ip_online(ip):
                print(ip)
                offline_ip.append(ip)
    return offline_ip


def get_all_net_config():
    ips = get_miner_net_config_by_box(11)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(get_miner_net_config, ips))


def change_work_mode_list():

    ip_list = txt_2_list('fans.txt')
    online_count = 0
    offline_ips = []  # 存储离线的 IP

    # 使用线程池并发
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_ip = {executor.submit(change_work_mode, ip): ip for ip in ip_list}
        # for future in as_completed(future_to_ip):
        #     ip = future_to_ip[future]
        #     if future.result():
        #         online_count += 1
        #     else:
        #         offline_ips.append(ip)

    return None


if __name__ == '__main__':
    change_work_mode_list()
