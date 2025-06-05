#  找出所有的平均算力不为0但是实时算力为0的矿机
from hbt_miner.file_miner_tools_k import csv_2_list
from hbt_miner.miner_tools import reboot_miner


def get_all_0_hash_over_temp_miner():
    filtered = []
    data = csv_2_list(r'C:\Users\xiepe\Documents\soft\ASIC.BTCTools-v1.3.3\060202.csv')
    for row in data:
        actual_str = row[4].replace(' GH/s', '').strip()
        expected_str = row[5].replace(' GH/s', '').strip()

        # 处理空字符串：为空则视为 0
        actual = float(actual_str) if actual_str else 0
        expected = float(expected_str) if expected_str else 0

        if actual == 0 and expected != 0:
            filtered.append(row)

    # 输出符合条件的行
    for item in filtered:
        print(item[0], item[4], item[5])
    return filtered


if __name__ == '__main__':
    reboot_list = get_all_0_hash_over_temp_miner()
    for miner in reboot_list:
        reboot_miner(miner[0])
