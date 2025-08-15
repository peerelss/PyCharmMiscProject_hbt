from whatsminer import WhatsminerAccessToken, WhatsminerAPI

from hbt_miner.file_miner_tools_k import txt_2_list


def get_hash_rate_by_ip(ip):
    try:
        token = WhatsminerAccessToken(ip_address=ip)
        summary_json = WhatsminerAPI.get_read_only_info(access_token=token,
                                                        cmd="summary")
        if 'Msg' in summary_json:
            return [ip, summary_json['Msg']['MHS av'], 'success']
        elif 'SUMMARY' in summary_json:
            return [ip, summary_json['SUMMARY'][0]['MHS av'] * 1000 * 1000, 'success']

    except Exception as e:
        if '[WinError 10060' in str(e):
            return [ip, -1, '离线']
        return [ip, 0, str(e)]


for ip in txt_2_list('ip_list.txt'):
    print(get_hash_rate_by_ip(ip))