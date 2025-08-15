from whatsminer_trans import *
from whatsminer_interface import *

miner_port = 4433
miner_account = "admin"
miner_passwd = "admin"
miner_salt = ''
ip = '10.203.3.78'


def get_hash_rate_zero_by_ip(ip):
    try:
        whatsminer_api = WhatsminerAPIv3(miner_account, miner_passwd)
        whatsminer_tcp = WhatsminerTCP(ip, miner_port, miner_account, miner_passwd)
        whatsminer_tcp.connect()
        req_info = whatsminer_api.get_request_cmds("get.device.info", param="error-code")
        req_length = len(req_info)
        rsp_info = whatsminer_tcp.send(req_info, req_length)
        error_code = (rsp_info['msg']['error-code'])
        fault_code_str = "_".join([list(d.keys())[0] for d in error_code])
        print(error_code)

        result = [ip, 0, fault_code_str]
        return result
    except Exception as e:
        return [ip, 0, str(e)]


print(get_hash_rate_zero_by_ip('10.206.3.11'))
