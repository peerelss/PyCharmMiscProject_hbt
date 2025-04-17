import sys

import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, \
    QTableWidget, QTableWidgetItem, QCheckBox

from hbt_miner.curl_tools import change_miner_ip_high
from hbt_miner.file_miner_tools_k import txt_2_list


class MinerConfigApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('矿机配置工具')

        # 主布局
        main_layout = QVBoxLayout()

        # 网络配置部分
        network_layout = QHBoxLayout()
        network_layout.addWidget(QLabel('起始目标IP前缀:'))
        self.ip_start = QLineEdit('192.168.39')
        network_layout.addWidget(self.ip_start)
        network_layout.addWidget(QLabel('起始IP:'))
        self.ip_start = QLineEdit('1')
        network_layout.addWidget(self.ip_start)
        network_layout.addWidget(QLabel('子网掩码:'))
        self.subnet_mask = QLineEdit('255.255.240.0')
        network_layout.addWidget(self.subnet_mask)

        network_layout.addWidget(QLabel('网关IP:'))
        self.gateway_ip = QLineEdit('192.168.39.1')
        network_layout.addWidget(self.gateway_ip)

        network_layout.addWidget(QLabel('DNS:'))
        self.dns = QLineEdit('8.8.8.8')
        network_layout.addWidget(self.dns)

        main_layout.addLayout(network_layout)

        # 操作说明部分
        operation_layout = QHBoxLayout()
        operation_layout.addWidget(QLabel('工作模式:'))
        self.mode = QComboBox()
        self.mode.addItems(['Normal', 'Low Power'])
        operation_layout.addWidget(self.mode)

        self.clear_ip = QCheckBox('清空IP')
        operation_layout.addWidget(self.clear_ip)

        # 添加“开始监听”和“跳过”按钮
        self.start_listen = QPushButton('开始监听')
        self.skip = QPushButton('跳过')
        operation_layout.addWidget(self.start_listen)
        operation_layout.addWidget(self.skip)

        main_layout.addLayout(operation_layout)

        # 表格部分
        self.table = QTableWidget(5, 6)
        self.table.setHorizontalHeaderLabels(['行号', '当前IP', 'MAC地址', '目标IP', 'IP设置状态', '矿机型号'])
        main_layout.addWidget(self.table)

        # 按钮部分
        button_layout = QHBoxLayout()
        self.select_all = QPushButton('全选')
        self.restart = QPushButton('重启软件')
        self.import_btn = QPushButton('导入')
        self.export_btn = QPushButton('导出')
        button_layout.addWidget(self.select_all)
        button_layout.addWidget(self.restart)
        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.export_btn)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="517d6873129c6f9123f476c4bd84283d", uri="/cgi-bin/get_system_info.cgi", response="45782a78f62e6e6934cb5405da972164", qop=auth, nc=00000002, cnonce="b77e46ff962779da"',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i',
    }

    response = requests.get('http://10.11.1.1/cgi-bin/get_system_info.cgi', headers=headers)
    print(response.json())