import concurrent.futures
import csv
import ipaddress

import requests
import re

from hbt_miner.file_miner_tools_k import csv_2_list, data_2_excel, txt_2_list
from hbt_miner.miner_tools import get_log_from_ip, get_hlog_from_ip

pattern = r"Chain (\d+) only find (\d+) asic"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0',
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="c2c1faf413a1daf7a08793897594170f", uri="/cgi-bin/hlog.cgi", response="edf063fd54f411c49042e43fed843a5e", qop=auth, nc=0000006a, cnonce="7bcd49a69a971e0a"',
    'Connection': 'keep-alive',
    'Referer': 'http://10.82.1.134/',
    'Priority': 'u=0',
}


def parse_log(ip, log_list):
    # 定义错误模式及其对应的标签
    error_patterns = [
        ('endswith', 'asic, times 2', 'miss asci'),
        ('in', 'Not enough chain', 'Not enough chain'),
        #   ('endswith', 'ERROR_POWER_LOST: power voltage rise or drop, pls check!', 'ERROR_POWER_LOST'),
        #   ('in', 'ERROR_TEMP_TOO_HIGH', 'ERROR_TEMP_TOO_HIGH'),
      #  ('in', 'ERROR_FAN_LOST', 'ERROR_FAN_LOST'),
        #   ('endswith', 'nonce crc error', 'nonce crc error'),
        # ('endswith', 'eeprom load ret:0', 'eeprom load ret:0'),
        #    ('in', 'ERROR_SOC_INIT', 'ERROR_SOC_INIT'),
        #  ('endswith','recieve sig,15','recieve sig,15')
    ]

    for log_str in (log_list):
        log_str = str(log_str)

        for method, pattern, label in error_patterns:
            if ((method == 'endswith' and log_str.endswith(pattern)) or
                    (method == 'in' and pattern in log_str)):
                happen_date = log_str.split(' ')[0]
                print(ip, happen_date, label, log_str)
                return [ip, happen_date, label, log_str]

    return [ip, 'con not find error']  # 若未匹配任何错误


def get_first_miss_hash_asic_date(ip):
    try:
        log_text = get_hlog_from_ip(ip)
        log_list = log_text.split('\n')
        return parse_log(ip, (log_list))

    except Exception as e:
        print(ip, str(e))
        return [ip, str(e)]


def get_sn_by_ip(ip):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="d57a399a49bd504350cfac5bbe6cf1bc", uri="/cgi-bin/get_system_info.cgi", response="06bcb3d16ab9f99a3ebcbfc7591d134e", qop=auth, nc=0000003f, cnonce="bdad691365605bf0"',
        'Connection': 'keep-alive',
        'Referer': 'http://10.101.1.150/',
    }
    try:
        response = requests.get(f'http://{ip}/cgi-bin/get_system_info.cgi', headers=headers)
        return [ip, response.json()['serinum']]
    except Exception as e:
        return [ip, 'error']


def get_first_power_lost(ip):
    try:
        log_text = get_hlog_from_ip(ip)
        log_list = log_text.split('\n')
        for log_str in log_list:
            if str(log_str).endswith('ERROR_POWER_LOST: power voltage rise or drop, pls check!'):
                happen_date = str(log_str).split(' ')[0]
                print(ip, happen_date, log_str)
                return [ip, happen_date, log_str]
        return [ip, ""]

    except Exception as e:
        print(ip, str(e))
        return [ip, str(e)]


def all_miss_asic_ip():
    btc_tools_csv = csv_2_list(r'C:\Users\xiepe\Desktop\0505.csv')
    # filtered = [row for row in btc_tools_csv if len(row) > 5 and row[5] in ("0 GH/s", "")]
    # for row in filtered:
    #     print(row)

    filtered_names = [row[0] for row in btc_tools_csv if len(row) > 4 and row[4] in ("0 GH/s", "")]
    return filtered_names


def get_all_miss_():
    all_ip = all_miss_asic_ip()
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        results = list(executor.map(get_first_miss_hash_asic_date, all_ip))
    for res in results:
        print(res)
    return results


def get_all_power_lost():
    power_lost_ip = txt_2_list('fans.txt')
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        results = list(executor.map(get_first_miss_hash_asic_date, power_lost_ip))

    sorted_data = sorted(results, key=lambda row: ipaddress.ip_address(row[0]))
    data_2_excel(sorted_data)


def light_miner(ip):
    pass


def get_sn_by_ip_list():
    sn_ips = txt_2_list('fans.txt')
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        results = list(executor.map(get_sn_by_ip, sn_ips))
    return results


if __name__ == '__main__':
    get_all_power_lost()
# sn_result = get_sn_by_ip_list()
# data_2_excel(sn_result)
# print(get_sn_by_ip('10.101.1.150'))
