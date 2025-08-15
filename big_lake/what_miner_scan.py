import requests

cookies = {
    'sysauth': '7301d23c28ab3f07fdfa84362a956252',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'Connection': 'keep-alive',
    'Referer': 'https://10.203.2.32/cgi-bin/luci/admin/status/overview',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'sysauth=7301d23c28ab3f07fdfa84362a956252',
}

response = requests.get(
    'https://10.203.2.32/cgi-bin/luci/admin/status/btminerstatus',
    cookies=cookies,
    headers=headers,
    verify=False,
)
print(response.content)