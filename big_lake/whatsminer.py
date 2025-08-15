import schedule

from big_lake.save_to_mongodb import save_task_to_db
from hbt_miner.file_miner_tools_k import txt_2_list
from whatsminer_trans import *
from whatsminer_interface import *
import subprocess
import platform

miner_port = 4433
miner_account = "admin"
miner_passwd = "admin"
miner_salt = ''

whatsminer_api = WhatsminerAPIv3(miner_account, miner_passwd)


def ping_ip(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    try:
        result = subprocess.run(
            ["ping", param, "1", ip],
            capture_output=True,
            text=True,
            timeout=3  # 可选，防止死等
        )
        output = result.stdout.lower()

        # Windows 返回 "reply from"
        # Linux/Mac 返回 "ttl="
        if "reply from" in output or "ttl=" in output:
            return True
        return False
    except Exception:
        return False


# req_info = whatsminer_api.set_miner_service("restart");
# req_length = len(req_info)
# rsp_info = whatsminer_tcp.send(req_info, req_length)
# print(f"{rsp_info}")

# req_info = whatsminer_api.set_user_passwd("user1", "user1","abcde1");
# req_length = len(req_info)
# rsp_info = whatsminer_tcp.send(req_info, req_length)
# print(f"{rsp_info}")


# 0算力机器寻找错误码和解决意见
def get_hash_rate_zero_by_ip(ip):
    try:
        whatsminer_api = WhatsminerAPIv3(miner_account, miner_passwd)
        whatsminer_tcp = WhatsminerTCP(ip, miner_port, miner_account, miner_passwd)
        whatsminer_tcp.connect()
        req_info = whatsminer_api.get_request_cmds("get.device.info", param="error-code")
        req_length = len(req_info)
        rsp_info = whatsminer_tcp.send(req_info, req_length)
        error_code = (rsp_info['msg']['error-code'])
        return [ip, 0, error_code]
    except Exception as e:
        return [ip, 0, str(e)]


def get_miner_hash_rate_rt_by_ip(ip):
    try:
        if not ping_ip(ip):
            return [ip, -1, 'offline']
        miner_ip = ip
        whatsminer_tcp = WhatsminerTCP(miner_ip, miner_port, miner_account, miner_passwd)
        whatsminer_tcp.connect()

        req_info = whatsminer_api.get_request_cmds("get.miner.status", param="summary")
        req_length = len(req_info)
        rsp_info = whatsminer_tcp.send(req_info, req_length)
        hash_rate = rsp_info['msg']['summary']['hash-realtime']
        if rsp_info['code'] == 0:
            #   print(f"{rsp_info}
            # if hash_rate > 0:
            return [ip, hash_rate, 'success']
        #:
        #   return get_hash_rate_zero_by_ip(ip)
        else:
            print(f"invalid msg {rsp_info}")
            exit()
    except Exception as e:
        return [ip, 0, str(e)]


def job():
    start = time.time()  # 记录开始时间
    result = map(get_miner_hash_rate_rt_by_ip, txt_2_list('ip_list.txt'))
    result_data = [row for row in result if row[1] <= 0]
    for d in result_data:
        print(d)
    save_task_to_db(result_data)
    # print(get_miner_pool_by_ip('10.0.10.1'))
    # get_all_miner_pool_config()
    end = time.time()  # 记录结束时间
    print(f"耗时: {end - start:.2f} 秒")


if __name__ == "__main__":
    job()
    schedule.every(10).minutes.do(job)

    print("定时任务已启动，每10分钟执行一次。")
    job()  # 启动时先跑一次

    # 循环执行
    while True:
        schedule.run_pending()
        time.sleep(1)
