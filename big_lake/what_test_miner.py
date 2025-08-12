from whatsminer import WhatsminerAccessToken, WhatsminerAPI

ip = '10.202.1.58'


def get_hash_by_ip(ip):
    try:
        token = WhatsminerAccessToken(ip_address=ip)
        summary_json = WhatsminerAPI.get_read_only_info(access_token=token,
                                                        cmd="summary")
        return [ip, summary_json['Msg']['MHS 15m'], 'success']
    except Exception as e:
        return [ip, 0, str(e)]


print(get_hash_by_ip(ip))
