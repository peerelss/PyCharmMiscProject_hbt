import os

def is_miner_online(ip):
    response = os.system(f"ping -n 1 {ip}")
    return response == 0

boxs=[11,12,21,22,31,32,41,42,51,52,61,62,71,72,81,82,91,92,101,102]
ip_3=[1,2,10,11]


ip = "10.11.1.1"

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    if is_miner_online(ip):
        print(f"矿机 {ip} 在线")
    else:
        print(f"矿机 {ip} 离线")

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
