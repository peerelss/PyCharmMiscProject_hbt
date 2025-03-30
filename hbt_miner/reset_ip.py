import requests
import json
import os.path
import re
from collections import Counter
import logging
from datetime import datetime
import csv
import pandas as pd

from hbt_miner.curl_tools import change_miner_ip
from hbt_miner.file_miner_tools_k import csv_2_list, txt_2_list, data_2_excel

# 从 xls里读取 sn应该对应的ip
# 从xls 里读取 ip列表
# 从ip列表里获取sn
# 根据sn找到正确的ip，并设置ip

csv_path = r'C:\Users\MSI\Downloads\Compressed\ASIC.BTCTools-v1.3.3\hbt_total_ip.csv'

xlsx_path = r'C:\Users\MSI\Downloads\hbt矿机状态.xlsx'


def ip_form_xlsx_by_box_no(box_no):
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # 跳过第一行（标题行）
            next(reader)
            lines = [row[0] for row in reader]
            filtered_ips = [ip for ip in lines if ip.split(".")[1] == box_no]
            return filtered_ips
    else:
        logging.warning(f'{csv_path}   not exist')


def get_ip_and_sn_from_xlsx(sheet_name):
    try:
        # 读取 Excel 文件中的指定工作表
        df = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None)
        # 将 DataFrame 转换为二维数组
        data = df.values.tolist()
        return data
    except Exception as e:
        print(f"读取 Excel 文件时出错: {e}")
        return None


def convert_number(num):
    row = num // 10  # 获取行号
    col = chr(64 + (num % 10))  # 64 是 'A' 之前的 ASCII 码，1 对应 'A'
    return f"{row}{col}"


def get_sn_by_ip(ip):
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
        return


def start_task():
    result_sns = get_ip_and_sn_from_xlsx('8A')
    result_ips = ip_form_xlsx_by_box_no('81')
    for ip in result_ips:
        sn_ip = get_sn_by_ip(ip)
        if sn_ip:
            for sn in result_sns:
                try:
                    if isinstance(sn[1], str):
                        if len(sn_ip) > 15 and len(sn[1]) > 15:
                            if sn_ip[-9:] == sn[1][-9:]:
                                if ip != sn[0]:
                                    print(f"旧 ip : {ip} sn: {sn[1]}  新ip:{sn[0]}")
                                    print('准备改')
                                    change_miner_ip(str(ip).strip(), sn[0])
                    else:
                        print(print(f"{sn}发生未知错误: {sn}"))
                except Exception as e:
                    print(f"{sn_ip}发生未知错误: {sn}")
                    return


def reset_by_csv(csv_path):
    target_data = csv_2_list(r'C:\Users\MSI\Desktop\72.csv')
    for tar in target_data:
        if tar and len(tar[1]) > 7 and tar[1] != tar[3]:
            change_miner_ip(tar[1], tar[3])

    result_sns = get_ip_and_sn_from_xlsx('4A')

    ips = txt_2_list(r'fans.txt')
    sn_list = []
    for ip in ips:
        sn_list.append([ip, get_sn_by_ip(ip)])
    for sn_i in sn_list:
        if sn_i and sn_i[1] and len(sn_i) > 1 and len(sn_i[1]) > 14:
            for sn in result_sns:
                if isinstance(sn[1], str):
                    if sn_i[1][-7:] == sn[1][-7:]:
                        print(sn, sn_i)
                        change_miner_ip(sn_i[0], sn[0])


if __name__ == '__main__':
    data = [['10.101.2.164', [0, 6000, 6000, 6000]],
            ['10.101.2.150', [5550, 5320, 5450, 0]],
            ['10.101.1.121', [6000, 0, 6000, 6000]],
            ['10.101.1.47', [5490, 5960, 0, 5970]],
            ['10.82.2.159', [0, 0, 5310, 5380]],
            ['10.81.1.87', [5990, 6000, 0, 5450]],
            ['10.81.1.6', [5540, 5340, 5530, 0]],
            ['10.72.2.157', [0, 5330, 5490, 5380]],
            ['10.72.2.45', [6000, 5980, 3640, 5410]],
            ['10.72.1.163', [6000, 5970, 6000, 0]],
            ['10.62.2.24', [0, 2350, 5910, 5930]],
            ['10.61.2.12', [6000, 0, 5500, 5910]],
            ['10.51.2.103', [0, 5670, 5730, 5790]],
            ['10.51.1.132', [5950, 0, 5980, 5900]],
            ['10.42.2.168', [5730, 5790, 0, 5790]],
            ['10.42.2.139', [5960, 5940, 1480, 5940]],
            ['10.42.1.85', [5360, 6000, 6000, 0]],
            ['10.41.2.6', [5400, 5470, 0, 5570]],
            ['10.41.1.95', [6000, 5380, 6000, 0]],
            ['10.32.2.76', [6000, 6000, 6000, 0]],
            ['10.31.1.67', [5960, 0, 5950, 6000]]]
    data_2_excel(data)
