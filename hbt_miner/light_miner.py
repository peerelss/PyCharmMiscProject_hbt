from hbt_miner.file_miner_tools_k import txt_2_list, light_miner
import concurrent.futures
import csv
import requests
import re




if __name__ == '__main__':
    light_ips=txt_2_list('lights.txt')
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        results = list(executor.map(light_miner, light_ips))