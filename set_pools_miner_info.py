from whatsminer import WhatsminerAccessToken, WhatsminerAPI


def set_miner_pools_info_by_ip(ip):
    token = WhatsminerAccessToken(ip_address=ip,
                                  admin_password="the_admin_passwd")


if __name__ == "__main__":
    pass
