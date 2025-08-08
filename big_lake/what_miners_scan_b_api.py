from whatsminer import WhatsminerAccessToken, WhatsminerAPI

from hbt_miner.file_miner_tools_k import txt_2_list


def get_hash_rate_by_ip(ip):
    try:
        token = WhatsminerAccessToken(ip_address=ip)
        summary_json = WhatsminerAPI.get_read_only_info(access_token=token,
                                                        cmd="summary")
        return [ip, summary_json['Msg']['MHS 15m'], 'success']
    except Exception as e:
        return [ip, 0, str(e)]


if __name__ == '__main__':
    ip_list = txt_2_list('ip_list.txt')
    for ip in ip_list:
        result = get_hash_rate_by_ip(ip)
        if result[1] == 0:
            print(result)
