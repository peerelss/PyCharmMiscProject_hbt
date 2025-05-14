import sys
import threading
import socket

from PyQt5.QtCore import pyqtSignal, QObject
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


# 信号类：用于接收 IP 和状态
class IpSignal(QObject):
    ip_received = pyqtSignal(str)


class StatusSignal(QObject):
    status_changed = pyqtSignal(str)


class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP 配置工具")
        self.resize(400, 350)
        self._init_ui()

        # 初始化监听相关变量
        self.listening = True
        self.listener_socket = None
        self.ip_signal = IpSignal()
        self.ip_signal.ip_received.connect(self.update_old_ip)
        self.status_signal = StatusSignal()
        self.status_signal.status_changed.connect(self.set_status_text)
        self.set_new_ip_prefix()
        self.start_ip_listener()

    def _init_ui(self):
        main_layout = QVBoxLayout()

        # 旧 IP
        old_ip_layout = QHBoxLayout()
        old_ip_layout.addWidget(QLabel("旧 IP:"))
        self.old_ip_edit = QLineEdit()
        self.old_ip_edit.setPlaceholderText("例如：192.168.1.100")
        old_ip_layout.addWidget(self.old_ip_edit)
        main_layout.addLayout(old_ip_layout)

        # 新 IP
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

        # 状态标签
        self.status_label = QLabel("监听状态：未启动")
        main_layout.addWidget(self.status_label)

        # 停止监听按钮
        self.stop_button = QPushButton("停止监听")
        self.stop_button.clicked.connect(self.stop_listening)
        main_layout.addWidget(self.stop_button)

        # 重新开始监听按钮
        self.restart_button = QPushButton("重新开始监听")
        self.restart_button.clicked.connect(self.restart_listening)
        main_layout.addWidget(self.restart_button)

        # 结果框
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

        try:
            result = change_miner_ip(old_ip, new_ip)
            self.old_ip_edit.clear()
            self.new_ip_edit.clear()
            self.result_box.append(result)
            self.set_new_ip_prefix()
        except Exception as ex:
            self.result_box.append(f"配置失败：{ex}")

    def update_old_ip(self, ip):
        self.old_ip_edit.setText(ip)
        self.result_box.append(f"接收到 IP：{ip}")

    def set_status_text(self, text):
        self.status_label.setText(f"监听状态：{text}")

    def start_ip_listener(self):
        thread = threading.Thread(target=self.listen_on_port, daemon=True)
        thread.start()

    def listen_on_port(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("0.0.0.0", 14235))
                s.listen(5)
                s.settimeout(1.0)
                self.listener_socket = s
                self.status_signal.status_changed.emit("监听中（端口 14235）")

                while self.listening:
                    try:
                        conn, addr = s.accept()
                        ip = addr[0]
                        self.ip_signal.ip_received.emit(ip)
                        conn.close()
                    except socket.timeout:
                        continue
        except Exception as e:
            self.status_signal.status_changed.emit(f"监听失败：{e}")

    def stop_listening(self):
        self.listening = False
        if self.listener_socket:
            try:
                self.listener_socket.close()
            except Exception as e:
                print(f"关闭 socket 时出错：{e}")
        self.status_signal.status_changed.emit("已停止")
        self.result_box.append("监听已手动停止。")

    def restart_listening(self):
        if self.listening:
            self.result_box.append("监听已经在运行中。")
            return
        self.listening = True
        self.result_box.append("尝试重新开始监听...")
        self.start_ip_listener()

    def set_new_ip_prefix(self):
        try:
            # 获取本机 IP（尝试连接外网以确定主 IP）
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()

            # 提取前三段
            prefix = ".".join(local_ip.split(".")[:3]) + "."
            self.new_ip_edit.setText(prefix)
            self.result_box.append(f"本机 IP 前缀自动填写为：{prefix}")
        except Exception as e:
            self.result_box.append(f"获取本机 IP 失败：{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ConfigWindow()
    win.show()
    sys.exit(app.exec_())
