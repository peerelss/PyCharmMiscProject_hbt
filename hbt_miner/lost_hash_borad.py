import concurrent
import ast
import csv
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


def get_first_miss_hash_asic_date(ip):
    try:
        log_text = get_hlog_from_ip(ip)
        log_list = log_text.split('\n')
        for log_str in reversed(log_list):
            if str(log_str).endswith('asic, times 2'):
                happen_date = str(log_str).split(' ')[0]
                print(ip, happen_date, 'miss asci', log_str)
                return [ip, happen_date, 'miss asci', log_str]
            elif str(log_str).endswith('ERROR_POWER_LOST: power voltage rise or drop, pls check!'):
                happen_date = str(log_str).split(' ')[0]
                print(ip, happen_date, 'ERROR_POWER_LOST', log_str)
                return [ip, happen_date, 'ERROR_POWER_LOST', log_str]
        return [ip, ""]

    except Exception as e:
        print(ip, str(e))
        return [ip, str(e)]


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
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(get_first_miss_hash_asic_date, all_ip))
    for res in results:
        print(res)
    return results


def get_all_power_lost():
    power_lost_ip = txt_2_list('fans.txt')
    result_list = []
    for ip in power_lost_ip:
        result_list.append(get_first_miss_hash_asic_date(ip))
    data_2_excel(result_list)


def light_miner(ip):
    pass


if __name__ == '__main__':
    get_all_power_lost()
