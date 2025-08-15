from pymongo import MongoClient

from hbt_miner.file_miner_tools_k import txt_2_list

MONGODB_URL = 'mongodb+srv://kevin_miner_test:Peerless123@cluster0.458zxp3.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(MONGODB_URL)

db = client["miner_db_big_lake"]  # 数据库名
collection = db["miners_big_lake"]  # 集合名

# 你的 IP 列表
from datetime import datetime


def insert_all_data():
    ip_list = txt_2_list('ip_list.txt')
    collection.delete_many({})
    print("数据库已清空")
    # 生成要插入的文档列表
    docs = []
    for ip in ip_list:
        parts = ip.split(".")
        if len(parts) != 4:
            print(f"无效 IP: {ip}")
            continue
        miner_box_id = int(parts[1])  # 第二个数字当矿箱ID
        docs.append({
            "ip": ip,
            "miner_box_id": miner_box_id
        })

    # 批量插入 MongoDB
    if docs:
        result = collection.insert_many(docs)
        print(f"已插入 {len(result.inserted_ids)} 条数据")
    else:
        print("没有有效数据可插入")


def find_ip_by_box_id():
    result = collection.update_many(
        {"miner_box_id": 0},  # 查询条件
        {"$set": {"miner_box_id": "B2"}}  # 更新操作
    )


def save_task_to_db(result_task):
    if (len(result_task)) == 0:
        return
    time_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    collection = db["miners_big_lake_task"]  # 集合名
    collection.delete_many(
        {}
    )
    documents = [{"ip": item[0], "hash_rate": item[1], "status": item[2], 'timestamp': time_update} for item in
                 result_task]
    result = collection.insert_many(documents)


if __name__ == "__main__":
    find_ip_by_box_id()
