from hbt_miner.curl_tools import change_miner_ip, change_miner_ip_high
import concurrent.futures


def generate_ips():
    """生成初始IP列表，按从左到右，从上到下排列"""
    ips = []
    for rack in range(1, 3):  # 1.x 和 2.x 两个网段
        for i in range(1, 169):  # 每个网段168个IP
            ips.append(f"{rack}.{i}")
    return ips


def reorder_ips(ips):
    """重新排列IP地址，使其按从右到左，从上到下排列，并且每一格从右到左，并列出新旧IP的对应关系"""
    new_order = []
    mapping = {}
    racks = [ips[i * 42:(i + 1) * 42] for i in range(8)]  # 分成8个架子，每个42个IP

    for rack in reversed(racks):  # 从右到左遍历架子
        grid = [rack[i * 6:(i + 1) * 6] for i in range(7)]  # 每个架子分成7格，每格6个IP
        for row in grid:  # 从上到下遍历格子
            new_order.extend(reversed(row))  # 使每一格内的IP也从右到左

    for old, new in zip(ips, new_order):
        mapping[old] = new

    return mapping


def get_new_ip(old_ip):
    """输入旧IP，返回新IP"""
    original_ips = generate_ips()
    mapping = reorder_ips(original_ips)
    return mapping.get(old_ip, "IP not found")


def main():
    original_ips = generate_ips()
    mapping = reorder_ips(original_ips)
    for old, new in mapping.items():
        print(f"{old} -> {new}")


def change_ip():
    pre_str = '10.22.'
    tar_ips = []
    for i in range(3, 5):
        for j in range(1, 169):
            str_old = f'{i}.{j}'
            old_ip = pre_str + str_old
            new_ip = pre_str + (str_old).replace('4.', '2.').replace('3.', '1.')
            print(f'old_ip: {old_ip};new_ip: {new_ip}')
            tar_ips.append([old_ip, new_ip])
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(change_miner_ip_high, tar_ips))



if __name__ == "__main__":
    change_ip()
