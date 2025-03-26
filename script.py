import subprocess
import platform
import os
import csv
import pandas as pd

from hbt_miner.curl_tools import change_miner_ip


def get_old_ip_and_new_ip_from_csv(csv_path):
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8', errors="ignore") as file:
            reader = csv.reader(file)
            # 跳过第一行（标题行）
            next(reader)
            lines = [[row[1], row[3]] for row in reader]
            return lines
    else:
        print(f'{csv_path}   not exist')


xlsx_path = r'C:\Users\MSI\Documents\luna\3A.xlsx'


def get_old_ip_and_new_ip_from_xlsx():
    try:
        # 读取 Excel 文件中的指定工作表
        df = pd.read_excel(xlsx_path, header=None, skiprows=1)
        df.fillna("0", inplace=True)
        # 将 DataFrame 转换为二维数组
        data = df.values.tolist()
        return data
    except Exception as e:
        print(f"读取 Excel 文件时出错: {e}")
        return None




if __name__ == '__main__':
    ips_list = get_old_ip_and_new_ip_from_csv(r'C:\Users\MSI\Documents\cumby\81.csv')
    # ips_list2 = get_old_ip_and_new_ip_from_xlsx()
    for ip in ips_list:
        if ip[0] and len(ip[0]) > 7 and len(ip[1]) > 7:
            if ip[0] != ip[1]:
                print(ip)
                change_miner_ip(ip[0], ip[1])

# for ip in ips_list:
#     if len(ip[0]) > 7 and len(ip[1]) > 7:
#        change_miner_ip(ip[1], ip[1].replace("10.22.3", "10.22.1").replace('10.22.4', '10.22.2'))
