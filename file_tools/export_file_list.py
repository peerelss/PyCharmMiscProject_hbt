import os

# 指定目标文件夹
folder_path = r"E:\pk"

# 获取所有文件（包含子目录）
file_names = []
for root, _, files in os.walk(folder_path):
    for file in files:
        file_names.append(os.path.relpath(os.path.join(root, file), folder_path))

# 指定导出文件路径
output_file = "file_list.txt"

# 写入文本文件
with open(output_file, "w", encoding="utf-8") as f:
    for file_name in file_names:
        f.write(file_name + "\n")

print(f"所有文件名（包含子目录）已导出到: {output_file}")
