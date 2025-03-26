import requests
import pandas as pd
import os
import csv
import concurrent.futures


# txt 2 list
def txt_2_list(txt_path):
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()  # 每行作为列表元素
            lines = [line.strip() for line in lines]  # 去掉换行符
        return lines
    except Exception as e:
        print(f"读取 Excel 文件时出错: {e}")
        return []


# data 2 excel
def data_2_excel(data_result):
    df = pd.DataFrame(data_result)
    # 保存为 Excel 文件
    df.to_excel("output.xlsx", index=False, header=False)
    print("Excel 文件已生成：output.xlsx")


def multi_task(fun_foo, data_bar):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(fun_foo, data_bar))

    return results
