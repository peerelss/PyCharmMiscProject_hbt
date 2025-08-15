import asyncio
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pymongo import MongoClient
import schedule
import time
import os
import logging
from dotenv import load_dotenv
import logging

BOT_TOKEN = '5854997437:AAEo96sEDCsDoCGG2vWBw_3fudGCulRBpTU'
TOKEN_Test = '5802231356:AAGomB_cjbTKCNX4kDbnUykgRC2lGaI2GKk'
CHAT_ID = "750326239"
TOKEN = '5854997437:AAEo96sEDCsDoCGG2vWBw_3fudGCulRBpTU'
# 加载环境变量
load_dotenv()
logger = logging.getLogger(__name__)
# 获取 MongoDB URL
mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')  # 如果没有设置环境变量，默认使用 localhost
from telegram import Bot

# MongoDB连接设置
mongo_client = MongoClient(mongodb_url)
db = mongo_client['miner_monitor']  # 数据库名
collection = db['box_status']  # 集合名


def send_telegram_alert(bot_token, chat_id, message):
    try:
        async def send():
            bot = Bot(token=bot_token)
            await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')

        asyncio.run(send())
        logging.info("Telegram 消息发送成功")
    except Exception as e:
        logging.error(f"Telegram 消息发送失败：{e}")


def is_ip_online(ip_address):
    try:
        output = subprocess.check_output(["ping", "-n", "3", "-w", "500", ip_address], stderr=subprocess.STDOUT,
                                         universal_newlines=True)
        if "TTL=" in output:
            return True
    except subprocess.CalledProcessError:
        pass
    return False


def generate_ip_list(ip_segment):
    base_ip = f"10.{ip_segment}"
    ip_list = []
    for i in range(1, 169):
        ip_list.append(f"{base_ip}.1.{i}")
        ip_list.append(f"{base_ip}.2.{i}")
    return ip_list


def count_online_ips(ip_segment):
    ip_list = generate_ip_list(ip_segment)
    online_count = 0
    offline_ips = []  # 存储离线的 IP

    # 使用线程池并发
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_ip = {executor.submit(is_ip_online, ip): ip for ip in ip_list}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            if future.result():
                online_count += 1
            else:
                offline_ips.append(ip)

    return online_count, offline_ips


def get_last_record():
    # 获取最近一次的记录
    last_record = collection.find_one(sort=[("timestamp", -1)])
    return last_record


def compare_with_last_record(current_data, last_data):
    # 比较当前数据和上一次数据
    reduced_boxes = []
    for current_box in current_data:
        for last_box in last_data["boxes"]:
            if current_box["box"] == last_box["box"]:
                # 计算在线数量变化
                if current_box["online_count"] < last_box["online_count"] * 0.8:  # 减少超过20%
                    reduced_boxes.append({
                        "box": current_box["box"],
                        "previous_count": last_box["online_count"],
                        "current_count": current_box["online_count"]
                    })
    return reduced_boxes


def scan_all_boxes_and_save(box_list):
    now = datetime.now()  # 获取统一时间戳
    records = []
    offline_ips_per_box = {}

    # 扫描每个矿箱
    for box in box_list:
        print(f"Scanning box {box}...")
        online_count, offline_ips = count_online_ips(box)
        record = {
            "box": box,
            "online_count": online_count,
            "offline_ips": offline_ips  # 保存离线的 IP
        }
        records.append(record)
        offline_ips_per_box[box] = offline_ips

    # 加入统一时间戳到整个记录
    result = {
        "timestamp": now,
        "boxes": records
    }

    # 获取上一次的记录
    last_record = get_last_record()

    if last_record:
        reduced_boxes = compare_with_last_record(records, last_record)
        if reduced_boxes:
            print("Boxes with significant decrease in online count:")
            for box in reduced_boxes:
                print(f"Box {box['box']} reduced from {box['previous_count']} to {box['current_count']}")
        else:
            print("No significant decrease in online counts.")

        # 比较离线 IP 的变化
        for box in box_list:
            last_offline_ips = None
            for last_box in last_record["boxes"]:
                if last_box["box"] == box:
                    last_offline_ips = last_box.get("offline_ips", [])
                    break

            if last_offline_ips:
                newly_offline = set(offline_ips_per_box[box]) - set(last_offline_ips)
                new_offline_count = len(newly_offline)
                if new_offline_count > 5:
                    logger.info(f"Box {box} has new offline IPs: {newly_offline}")
                    message = f"⚠️ <b>矿机告警</b>：Box {box} 新增 <b>{new_offline_count}</b> 台设备离线！请及时处理！"
                    send_telegram_alert(BOT_TOKEN, CHAT_ID, message)
                if newly_offline:
                    print(f"Box {box} has new offline IPs: {newly_offline}")
                else:
                    print(f"Box {box} has no new offline IPs.")
            else:
                print(f"Box {box} had no previous record of offline IPs.")

    # 保存当前数据到MongoDB
    collection.insert_one(result)
    print(f"Inserted data for all boxes with timestamp {now} into MongoDB.")


# 每半小时执行一次


# 设置每半小时执行一次 job

if __name__ == "__main__":
    # 启动一个无限循环，定期执行 job
    pass
