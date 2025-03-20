from pymongo import MongoClient
from datetime import datetime
from hbt_miner.miner_tools import detect_box

# 连接 MongoDB
client = MongoClient("mongodb://localhost:27017/")  # 替换为你的 MongoDB 连接地址
db = client["mining_db"]  # 选择数据库
box_list = ['11', '12', '21', '22', '31', '32', '41', '42', '51', '52', '61', '62', '71', '72', '81', '82', '91', '92',
            '101', '102']


def scan_and_insert(box_no):
    collection = db[box_no]  # 选择集合（表）
    collection.delete_many({})
    data = detect_box(box_no)
    formatted_data = [
        {"ip": item[0],
         "hash_rate": float(item[1]) if isinstance(item[1], str) else item[1],
         "status": item[2],
         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 添加时间
         }
        for item in data
    ]
    # 批量插入数据
    result = collection.insert_many(formatted_data)
    # 输出插入的 ID
    print("Inserted IDs:", result.inserted_ids)


def search_and_show_data(box_no):
    client = MongoClient("mongodb://localhost:27017/")  # 替换为你的 MongoDB 连接地址
    db = client["mining_db"]  # 选择数据库

    # 选择集合（类似于 SQL 的表）
    collection = db[box_no]

    # 查询所有数据
    cursor = collection.find()

    # 遍历并输出数据
    for doc in cursor:
        print(doc)


if __name__ == '__main__':
    for box in box_list:
        scan_and_insert(box)
    #search_and_show_data('11')
