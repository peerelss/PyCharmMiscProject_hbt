from pymongo import MongoClient
from datetime import datetime
from hbt_miner.miner_tools import detect_box
from collections import Counter

# 连接 MongoDB
client = MongoClient("mongodb://localhost:27017/")  # 替换为你的 MongoDB 连接地址
db = client["mining_db"]  # 选择数据库
box_list = ['11', '12', '21', '22', '31', '32', '41', '42', '51', '52', '61', '62', '71', '72', '81', '82', '91', '92',
            '101', '102']


def scan_and_insert(box_no):
    collection = db[box_no]  # 选择集合（表）
    data = detect_box(box_no)
    # 插入每个矿箱的统计数据
    counter = Counter(row[2] for row in data)
    counter['box_no'] = box_no
    collection_c = db["total_box"]
    existing_document = collection_c.find_one({"box_no": counter["box_no"]})

    if existing_document:
        # Update the existing document if found
        collection_c.update_one({"box_no": counter["box_no"]}, {"$set": counter})
        print(f"Document with box_no {counter['box_no']} updated.")
    else:
        # Insert a new document if not found
        collection_c.insert_one(counter)
        print(f"Document with box_no {counter['box_no']} inserted.")

    # 插入扫描的信息
    collection.delete_many({})
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


def get_total_box(box_no):
    data = detect_box(box_no)
    counter = Counter(row[2] for row in data)
    print(counter)


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
# search_and_show_data('11')
# scan_and_insert('11')
