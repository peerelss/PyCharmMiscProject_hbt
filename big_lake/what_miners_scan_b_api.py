from whatsminer import WhatsminerAccessToken, WhatsminerAPI
from concurrent.futures import ThreadPoolExecutor
import time
from collections import Counter

from hbt_miner.file_miner_tools_k import txt_2_list


def get_hash_rate_by_ip(ip):
    try:
        token = WhatsminerAccessToken(ip_address=ip)
        summary_json = WhatsminerAPI.get_read_only_info(access_token=token,
                                                        cmd="summary")
        return [ip, summary_json['Msg']['MHS 15m'], 'success']
    except Exception as e:
        return [ip, 0, str(e)]


def get_miner_pool_by_ip(ip):
    try:
        token = WhatsminerAccessToken(ip_address=ip)
        pools_json = WhatsminerAPI.get_read_only_info(access_token=token,
                                                      cmd="pools")
        pools = pools_json['POOLS']
        return [ip, 1, pools[0]['URL'], pools[0]['User'], pools[1]['URL'], pools[1]['User'], pools[2]['URL'],
                pools[2]['User']]

    except Exception as e:
        return [ip, 0, str(e)]


def get_all_miner():
    ip_list = txt_2_list('ip_list.txt')
    with ThreadPoolExecutor(max_workers=20) as executor:  # max_workers 可以根据网络和CPU情况调整
        result = list(executor.map(get_miner_pool_by_ip, ip_list))
    result_data = [row for row in result if row[1] == 0]
    for d in result_data:
        print(d)


def get_all_miner_pool_config():
    ip_list = txt_2_list('ip_list.txt')
    with ThreadPoolExecutor(max_workers=20) as executor:  # max_workers 可以根据网络和CPU情况调整
        pools_config = list(executor.map(get_miner_pool_by_ip, ip_list))
    result = [row for row in pools_config if row[1] == 1]
    third_values = [row[3] for row in result]
    # 统计次数
    count_result = Counter(third_values)
    filtered = [row for row in result if count_result[row[3]] > 1]

    for fi in filtered:
        print(fi)

    # 找出不合法矿池
    result = [row for row in result if row[2] != 'stratum+tcp://btc.poolhash.space:2001' and row[
        2] != 'stratum+tcp://btc-us.spiderpool.com:2309']
    if len(result) == 0:
        print('无非法矿池')
    for re in result:
        print(re)


def edit_pool_info(ip):
    try:
        token = WhatsminerAccessToken(ip_address=ip)
        pools_json = WhatsminerAPI.get_read_only_info(access_token=token,
                                                      cmd="pools")
        pools = pools_json['POOLS']
        result_json = WhatsminerAPI.exec_command()
    except Exception as e:
        return [ip, 'edit pools failure']


if __name__ == '__main__':
    start = time.time()  # 记录开始时间
    get_all_miner()
    # print(get_miner_pool_by_ip('10.0.10.1'))
    #get_all_miner_pool_config()
    end = time.time()  # 记录结束时间
    print(f"耗时: {end - start:.2f} 秒")
