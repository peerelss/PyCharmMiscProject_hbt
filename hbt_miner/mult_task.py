import asyncio
import aiohttp
from ipaddress import ip_address
import time  # <-- 新增

START_IP = '10.11.1.1'
END_IP = '10.11.1.168'
CONCURRENCY = 100
TIMEOUT = 2


def generate_ip_range(start_ip, end_ip):
    start = int(ip_address(start_ip))
    end = int(ip_address(end_ip))
    return [str(ip_address(ip)) for ip in range(start, end + 1)]


async def check_ip(ip, session, semaphore):
    url = f"http://{ip}"
    try:
        async with semaphore:
            async with session.get(url, timeout=TIMEOUT) as resp:
                if resp.status == 200:
                    print(f"[+] {ip} is ONLINE (HTTP 200)")
                    return ip
    except Exception:
        pass
    return None


async def main():
    start_time = time.time()  # <-- 记录开始时间

    ips = generate_ip_range(START_IP, END_IP)
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async with aiohttp.ClientSession() as session:
        tasks = [check_ip(ip, session, semaphore) for ip in ips]
        results = await asyncio.gather(*tasks)

    online_ips = [ip for ip in results if ip]

    print("\n✅ 在线 IP:")
    for ip in online_ips:
        print(ip)

    end_time = time.time()  # <-- 记录结束时间
    print(f"\n⏱️ 扫描耗时: {end_time - start_time:.2f} 秒")


if __name__ == "__main__":
    asyncio.run(main())
