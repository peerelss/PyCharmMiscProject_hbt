from whatsminer_trans import *
from whatsminer_interface import *

miner_port = 4433
miner_account = "admin"
miner_passwd = "admin"
miner_salt = ''
ip = '10.203.3.78'
whatsminer_api = WhatsminerAPIv3(miner_account, miner_passwd)
whatsminer_tcp = WhatsminerTCP(ip, miner_port, miner_account, miner_passwd)
whatsminer_tcp.connect()
req_info = whatsminer_api.get_request_cmds("get.device.info", param="error-code")
req_length = len(req_info)
rsp_info = whatsminer_tcp.send(req_info, req_length)
print(rsp_info['msg']['error-code'])
