from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin


def get_av_id(page):
    total_result = []
    for i in range(1, page + 1):
        total_result = total_result + (get_title_and_url(str(i)))
    result_str = formant_result(total_result)
    return result_str


def formant_result(result_list):
    str_list = ''
    for str_re in result_list:
        str_list = str_list + '\n' + str_re['alt']
    return str_list


def get_title_and_url(page):
    target_url = f"https://page={page}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="zh-CN"
        )
        page = context.new_page()
        page.goto(target_url)
        elements = page.query_selector_all("a.text-secondary")

        results = []

        for el in elements:
            href = el.get_attribute("href")
            alt = el.get_attribute("alt")
            text = el.inner_text().strip()

            # 处理相对链接为绝对链接
            full_href = urljoin(target_url, href) if href else None

            results.append({
                "href": full_href,
                "alt": alt,
                "text": text
            })

        # 输出结果

        browser.close()
        return results


if __name__ == '__main__':
    import socket

    # 设置广播地址和端口
    broadcast_ip = '255.255.255.255'
    broadcast_port = 14235

    # 要发送的内容（根据协议定义内容）
    message = b'\x01\x02\x03\x04'  # 举例的内容，根据具体协议更改

    # 创建 UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # 发送广播
    sock.sendto(message, (broadcast_ip, broadcast_port))

    print(f"已发送广播到 {broadcast_ip}:{broadcast_port}")
    sock.close()

