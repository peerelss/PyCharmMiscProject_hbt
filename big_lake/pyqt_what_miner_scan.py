import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel
)
from PyQt5.QtCore import Qt
from whatsminer import WhatsminerAccessToken, WhatsminerAPI

from datetime import datetime


class PingChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP在线检测 - Whatsminer方式")
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)  # 居中显示
        self.status_label.setStyleSheet("color: green; font-weight: bold;")

        self.left_text = QTextEdit()
        self.left_text.setPlaceholderText("请输入IP列表，每行一个IP")

        self.check_button = QPushButton("检测IP在线状态")
        self.check_button.clicked.connect(self.check_ips)

        # 用表格代替文本框，显示不在线IP和错误信息
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["IP地址", "算力 (MHS 15m)", "状态/错误信息"])
        self.table.horizontalHeader().setStretchLastSection(True)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.check_button)
        right_layout.addWidget(self.status_label)  # 提示文本框放这里，表格上方

        right_layout.addWidget(self.table)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_text)  # 左边固定宽度
        main_layout.addLayout(right_layout, 1)  # 右边占满剩余空间

        self.setLayout(main_layout)
        self.resize(700, 400)

    def check_ip_status(self, ip):
        try:
            token = WhatsminerAccessToken(ip_address=ip)
            summary_json = WhatsminerAPI.get_read_only_info(access_token=token,
                                                            cmd="summary")
            return [ip, summary_json['Msg']['MHS 15m'], 'success']
        except Exception as e:
            return [ip, 0, str(e)]

    def check_ips(self):
        ips = self.left_text.toPlainText().strip().splitlines()
        offline_list = []
        for ip in ips:
            ip = ip.strip()
            if not ip:
                continue
            res = self.check_ip_status(ip)
            if res[1] < 100*1000*1000:  # 算力为0，表示不在线
                offline_list.append(res)

        # 填充表格
        self.table.setRowCount(len(offline_list))
        for row, (ip, mhs, status) in enumerate(offline_list):
            self.table.setItem(row, 0, QTableWidgetItem(ip))
            self.table.setItem(row, 1, QTableWidgetItem(str(mhs)))
            self.table.setItem(row, 2, QTableWidgetItem(status))

        if len(offline_list) == 0:
            self.table.setRowCount(0)
            self.table.setRowCount(1)
            self.status_label.setText("扫描完毕")
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg = f"所有IP均在线 （更新时间：{now_str}）"
            self.table.setItem(0, 0, QTableWidgetItem(msg))
            self.table.setSpan(0, 0, 1, 3)
            for col in range(1, 3):
                self.table.setItem(0, col, QTableWidgetItem(""))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PingChecker()
    window.show()
    sys.exit(app.exec_())
