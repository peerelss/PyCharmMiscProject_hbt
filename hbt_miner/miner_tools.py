import json
import os.path
import re
from collections import Counter
import logging
from datetime import datetime
import csv

# 配置基本日志格式
logging.basicConfig(level=logging.INFO)
import requests

error_message = [
    'ERROR_TEMP_TOO_HIGH',  # 高温
    'Error, fan lost',  # 风扇故障
    'ERROR_POWER_LOST',  # 电源故障
    'ERROR_TEMP_TOO_LOW'  # 温差过大
]
reboot_message = [
    'ERROR_TEMP_TOO_HIGH',  # 高温
    'ERROR_POWER_LOST',  # 电源故障
    'ERROR_TEMP_TOO_LOW'  # 温差过大
]
pattern = r"Chain (\d+) only find (\d+) asic"


def get_hash_rate_from_ip(ip):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': 'Digest username=root, realm=antMiner Configuration, nonce=fa6b40de72f629bdf89863f75ef56e46, uri=/cgi-bin/summary.cgi, response=30e3d6a442b938be50ca664eb5895d26, qop=auth, nc=0000005b, cnonce=c5ee5839ceaadceb',
        'Connection': 'keep-alive',
        'Referer': f'http://{ip}/',
    }

    try:
        response = requests.get(f'http://{ip}/cgi-bin/summary.cgi', headers=headers, timeout=5)

        # 如果 HTTP 状态码不是 200，抛出异常
        response.raise_for_status()

        # 解析 JSON
        data = response.json()

        # 确保 'SUMMARY' 键存在
        if 'SUMMARY' in data and isinstance(data['SUMMARY'], list) and 'rate_5s' in data['SUMMARY'][0]:
            #  print(f"矿机 {ip} 5s算力: {data['SUMMARY'][0]['rate_5s']}")
            hash_rate_n = data['SUMMARY'][0]['rate_5s']
            error_s = data['SUMMARY'][0]['status']
            filtered_types = [item['type'] for item in error_s if item['code'] != 0]
            if hash_rate_n == 0:
                if 'network' in filtered_types:
                    return -2  # 网络问题
                elif 'temp' in filtered_types:
                    return -3  # 高温问题
                elif 'fans' in filtered_types:
                    return -4  # 风扇问题
            return hash_rate_n
        else:
            print(f"矿机 {ip} 返回的 JSON 数据不包含 'SUMMARY' 或 'rate_5s'")

    except requests.exceptions.Timeout:
        print(f"请求超时: 无法连接到矿机 {ip}")
        return -1

    except requests.exceptions.ConnectionError:
        print(f"连接错误: 矿机 {ip} 可能离线或 IP 地址错误")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP 错误: {e}")

    except json.decoder.JSONDecodeError:
        print(f"JSON 解析错误: 矿机 {ip} 返回的内容不是有效的 JSON")

    except KeyError as e:
        print(f"KeyError: {e} - JSON 数据结构可能已更改")

    except Exception as e:
        print(f"发生未知错误: {e}")
    return 0


def get_log_from_ip(ip):
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
        response = requests.get(f'http://{ip}/cgi-bin/log.cgi', headers=headers, timeout=5)

        # 检查 HTTP 状态码
        response.raise_for_status()

        # 确保返回的内容不为空
        if not response.content:
            logging.warning(f"矿机 {ip} 返回的日志内容为空")
            return None

        # 尝试解码（如果需要）
        try:
            log_data = response.content.decode("utf-8")
        except UnicodeDecodeError:
            logging.warning(f"矿机 {ip} 返回的日志数据不是 UTF-8 编码")
            log_data = response.content  # 直接返回二进制数据

        return log_data

    except requests.exceptions.Timeout:
        logging.warning(f"请求超时: 无法连接到矿机 {ip}")
        return None

    except requests.exceptions.ConnectionError:
        logging.warning(f"连接错误: 矿机 {ip} 可能离线或 IP 地址错误")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"HTTP 错误: {e}")
        return None

    except Exception as e:
        print(f"发生未知错误: {e}")
        return None


def detect_error_from_url(log_text):
    if log_text:
        if 'ERROR_TEMP_TOO_HIGH' in log_text:
            return '高温问题'
        elif 'Error, fan lost' in log_text:
            return '风扇问题'
        elif 'ERROR_POWER_LOST' in log_text:
            return '电源问题'
        elif 'ERROR_TEMP_TOO_LOW' in log_text:
            return '温差过大'
        elif 'bad chain id' in log_text:
            return '算力板故障'
        match = re.search(pattern, log_text)
        if match:
            chain_id = match.group(1)  # 提取 Chain ID
            asic_count = match.group(2)  # 提取 ASIC 数量
            # print(f"匹配成功: Chain {chain_id}, 发现 {asic_count} 颗 ASIC")
            return '掉芯片'
    return 'unknown'


def detect_ip(ip):
    hash_rate_5s = get_hash_rate_from_ip(ip)
    if hash_rate_5s > 0:
        return [ip, str(hash_rate_5s), 'normal']
    elif hash_rate_5s == 0:
        log_txt = get_log_from_ip(ip)
        error_txt = detect_error_from_url(log_txt)
        if error_txt in reboot_message:
            reboot_miner(ip)
        return [ip, 0, error_txt]
    elif hash_rate_5s == -1:
        return [ip, -1, "离线"]
    elif hash_rate_5s == -2:
        return [ip, -2, "网络问题"]
    elif hash_rate_5s == -3:
        return [ip, -3, "高温问题"]
    elif hash_rate_5s == -4:
        return [ip, -4, "风扇问题"]
    else:
        return [ip, -1, "离线"]


def detect_box(txt_name):
    csv_path = r'C:\Users\MSI\Desktop\947.csv'
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # 跳过第一行（标题行）
            next(reader)
            lines = [row[0] for row in reader]
            filtered_ips = [ip for ip in lines if ip.split(".")[1] == txt_name]
            result_list = []
            for l in filtered_ips:
                if len(l) > 7:
                    result = detect_ip(l)
                    result_list.append(result)
            return result_list
    else:
        logging.warning(f'{csv_path}   not exist')


def reboot_miner(ip):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': 'Digest username=root, realm=antMiner Configuration, nonce=22217dd8940a927607b4233a247a52b6, uri=/cgi-bin/reboot.cgi, response=4f900550554ee411a6652e41933cf341, qop=auth, nc=00000038, cnonce=95f61bb5123f8297',
        'Connection': 'keep-alive',
        'Referer': f'http://{ip}/',
        'Priority': 'u=0',
    }

    response = requests.get(f'http://{ip}/cgi-bin/reboot.cgi', headers=headers)
    logging.info(f" : 矿机 {ip} 重启")
    logging.info(response)


def start_scan_task():
    # 生成时间戳格式的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{timestamp}.txt"
    with open(file_name, "a", encoding="utf-8") as file:
        for i in range(1, 11):
            for j in range(1, 3):
                box_result = detect_box(i * 10 + j)
                for box in box_result:
                    if box[2] == "电源问题" or box[2] == '高温问题':
                        reboot_miner(box[0])
                        logging.info(f'reboot {box[0]}')
                    logging.info(box)
                    file.write(str(box) + "\n")
                counter = Counter(row[2] for row in box_result)
                logging.warning(counter)
                file.write(str(counter) + "\n")


def scan_box_no(box_no):
    box_result = detect_box(box_no)
    for box in box_result:
        if box[2] == "电源问题" or box[2] == '高温问题' or box[2] == 'ERROR_TEMP_TOO_LOW':
            reboot_miner(box[0])
            logging.info(f'reboot {box[0]}')
        logging.info(box)
    counter = Counter(row[2] for row in box_result)
    logging.warning(counter)


def get_ip_from_csv(box_no):
    # 读取 CSV 文件并提取第一列
    csv_path = r'C:\Users\AAA\Downloads\BTCTools-v1.3.4\\' + str(box_no) + '.csv'
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # 跳过第一行（标题行）
            next(reader)
            first_column = [row[0] for row in reader]

        return first_column
    else:
        logging.warning(f'{csv_path}   not exist')


if __name__ == '__main__':
    # 生成时间戳格式的文件名
    scan_box_no('62')
    # get_ip_from_csv(102)
    #print(get_hash_rate_from_ip("10.62.11.61"))
