from hbt_miner.file_miner_tools_k import txt_2_list, light_miner
import concurrent.futures
import csv
import requests
import re
import requests
from requests.auth import HTTPDigestAuth


def get_miner_detail():
    url = "http://10.11.1.7/cgi-bin/stats.cgi"
    username = "root"
    password = "root"

    response = requests.get(url, auth=HTTPDigestAuth(username, password))

    if response.status_code == 200:
        print("✅ 请求成功！")
        print(response.text)
    else:
        print(f"❌ 请求失败，状态码: {response.status_code}")


if __name__ == '__main__':
    light_ips = txt_2_list('lights.txt')
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        results = list(executor.map(light_miner, light_ips))
# get_miner_detail()
