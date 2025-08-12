import csv

data_list = []
with open('shenma.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        data_list.append(row)

for da in data_list:
    for d in da:
        if len(d) > 7:
            print(d)
