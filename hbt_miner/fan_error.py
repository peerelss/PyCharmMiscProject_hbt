import requests
import pandas as pd
import os
import csv

from hbt_miner.curl_tools import change_miner_ip
from hbt_miner.file_miner_tools_k import multi_task

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'Authorization': 'Digest username=root, realm=antMiner Configuration, nonce=5434d219f9cf57856d727bb10c608094, uri=/cgi-bin/stats.cgi, response=a24614ec7f918c96db70cd8ca0eccbaa, qop=auth, nc=0000004a, cnonce=0bb5916b63775c42',
    'Connection': 'keep-alive',
    'Referer': 'http://10.12.2.101/',
}


def get_fan_by_ip(ip):
    try:
        response = requests.get(f'http://{ip}/cgi-bin/stats.cgi', headers=headers)
        fans = (response.json()['STATS'][0]['fan'])
        return [ip, fans]
    except Exception as e:
        print(f"读取 Excel 文件时出错: {e}")
        return [ip]


# 将txt里的数据转化为列表
def txt_2_list(txt_path):
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()  # 每行作为列表元素
            lines = [line.strip() for line in lines]  # 去掉换行符
        return lines
    except Exception as e:
        print(f"读取 Excel 文件时出错: {e}")
        return []


def get_data_from_csv_file(csv_path):
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8', errors="ignore") as file:
            reader = csv.reader(file)
            # 跳过第一行（标题行）
            next(reader)
            data = [row for row in reader]  # 转换为二维数组
            return data
    else:
        print(f'{csv_path}   not exist')


def get_mac_from_ip(ip):
    try:
        response = requests.get(f'http://{ip}/cgi-bin/get_system_info.cgi', headers=headers)
        macaddr = (response.json()['macaddr'])
        return [ip, macaddr]
    except Exception as e:
        print(f"读取 Excel 文件时出错: {e}")
        return [ip, ]


def data_2_excel(data_result):
    df = pd.DataFrame(data_result)
    # 保存为 Excel 文件
    df.to_excel("output.xlsx", index=False, header=False)
    print("Excel 文件已生成：output.xlsx")


def detect_fan_list():
    fans_result = []
    for ip in ips_list:
        if len(ip) > 7:
            fans_result.append(get_fan_by_ip(ip))
    for fan in fans_result:
        print(fan)
    data_2_excel(fans_result)


if __name__ == '__main__':
    ips_list = txt_2_list('fans.txt')
    mac_list = []
    mac_list_target = get_data_from_csv_file(r'C:\Users\MSI\Documents\cumby\91.csv')
    result_mac = {row[2]: row[3] for row in mac_list_target}
    for ip in ips_list:
        if len(ip) > 7:
            mac_list.append(get_mac_from_ip(ip))
    task_list = []
    for mac in mac_list:
        new_ip = result_mac.get(mac[1], '')
        if len(new_ip) > 7:
            print(mac[0], new_ip)
            change_miner_ip(mac[0], new_ip)
        # task_list.append([mac[0], new_ip])
    # result_data = multi_task(change_miner_ip, task_list)
