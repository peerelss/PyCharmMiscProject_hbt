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
    target_url = f"https://missav123.com/dm23/cn/actresses/%E4%BA%8C%E5%AE%AB%E5%92%8C%E9%A6%99?page={page}"
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
    get_av_id(2)
