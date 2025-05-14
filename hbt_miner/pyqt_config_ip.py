import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QMessageBox,
)

from hbt_miner.curl_tools import change_miner_ip


class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP 配置工具")
        self.resize(400, 300)
        self._init_ui()

    def _init_ui(self):
        # 布局
        main_layout = QVBoxLayout()

        # 旧 IP 输入行
        old_ip_layout = QHBoxLayout()
        old_ip_layout.addWidget(QLabel("旧 IP:"))
        self.old_ip_edit = QLineEdit()
        self.old_ip_edit.setPlaceholderText("例如：192.168.1.100")
        old_ip_layout.addWidget(self.old_ip_edit)
        main_layout.addLayout(old_ip_layout)

        # 新 IP 输入行
        new_ip_layout = QHBoxLayout()
        new_ip_layout.addWidget(QLabel("新 IP:"))
        self.new_ip_edit = QLineEdit()
        self.new_ip_edit.setPlaceholderText("例如：192.168.1.101")
        new_ip_layout.addWidget(self.new_ip_edit)
        main_layout.addLayout(new_ip_layout)

        # 配置按钮
        self.config_button = QPushButton("点击配置")
        self.config_button.clicked.connect(self.on_config_clicked)
        main_layout.addWidget(self.config_button)

        # 结果显示文本框
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        main_layout.addWidget(self.result_box, stretch=1)

        self.setLayout(main_layout)

    def on_config_clicked(self):
        old_ip = self.old_ip_edit.text().strip()
        new_ip = self.new_ip_edit.text().strip()

        if not old_ip or not new_ip:
            QMessageBox.warning(self, "输入错误", "请同时填写旧 IP 和新 IP。")
            return


        # 下面只是示例：拼接输出
        try:
            result = change_miner_ip(old_ip, new_ip)
            # 模拟配置过程
            # 将结果追加到文本框
            self.result_box.append(result)
        except Exception as ex:
            self.result_box.append(f"配置失败：{ex}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ConfigWindow()
    win.show()
    sys.exit(app.exec_())
