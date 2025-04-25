import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt, QRegExp, QThread, pyqtSignal
from PyQt5.QtGui import QRegExpValidator

from k.py_spider import get_title_and_url, formant_result,get_av_id


class FetchWebTitleThread(QThread):
    """用于在后台获取网页标题的线程"""
    result_signal = pyqtSignal(str, str)  # 信号：成功时发送标题，失败时发送错误信息

    def __init__(self, url, number_param):
        super().__init__()
        self.url = url
        self.number_param = number_param

    def run(self):
        try:
            # 构造带参数的URL
            result_json = get_av_id(int(self.number_param))
            self.result_signal.emit(result_json, '')

        except requests.exceptions.RequestException as e:
            self.result_signal.emit('', f"网络请求错误: {str(e)}")
        except Exception as e:
            self.result_signal.emit('', f"发生未知错误: {str(e)}")


class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.fetch_thread = None  # 用于保存当前的线程对象

    def initUI(self):
        # 设置主窗口属性
        self.setWindowTitle('带参数的网页标题获取器')
        self.setGeometry(300, 300, 800, 600)

        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 输入框1 - 用于输入URL
        input1_layout = QHBoxLayout()
        self.label1 = QLabel('网页URL:')
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText('请输入有效的网页地址 (如: https://example.com)')
        input1_layout.addWidget(self.label1)
        input1_layout.addWidget(self.input1)

        # 输入框2 - 只能输入正整数
        input2_layout = QHBoxLayout()
        self.label2 = QLabel('URL参数:')
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText('请输入要添加到URL的正整数参数...')

        # 设置验证器，只允许输入1位或多位数字(正整数)
        reg_ex = QRegExp("^[1-9]\\d*$")
        input_validator = QRegExpValidator(reg_ex, self.input2)
        self.input2.setValidator(input_validator)

        input2_layout.addWidget(self.label2)
        input2_layout.addWidget(self.input2)

        # 按钮区域
        button_layout = QHBoxLayout()
        self.button1 = QPushButton('获取标题')
        self.button2 = QPushButton('清空')
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        # 文本框
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)  # 设置为只读
        self.text_output.setPlaceholderText('网页标题和结果将显示在这里...')

        # 将所有部件添加到主布局
        main_layout.addLayout(input1_layout)
        main_layout.addLayout(input2_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.text_output)

        # 设置主布局
        self.setLayout(main_layout)

        # 连接信号和槽
        self.button1.clicked.connect(self.on_button1_click)
        self.button2.clicked.connect(self.on_button2_click)

    def on_button1_click(self):
        # 检查URL输入
        url = self.input1.text().strip()
        if not url:
            QMessageBox.warning(self, '输入错误', '请输入有效的网页URL!')
            return

        # 检查URL格式 (简单验证)
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url  # 自动添加http前缀

        # 检查正整数输入
        if not self.input2.text():
            QMessageBox.warning(self, '输入错误', '请输入正整数参数!')
            return
        number_param = self.input2.text()

        # 显示正在获取的状态
        self.text_output.append(f"正在获取: {url}?param={number_param} ...")
        self.button1.setEnabled(False)  # 禁用按钮防止重复点击

        # 启动线程获取网页标题
        self.fetch_thread = FetchWebTitleThread(url, number_param)
        self.fetch_thread.result_signal.connect(self.handle_fetch_result)
        self.fetch_thread.finished.connect(self.cleanup_thread)
        self.fetch_thread.start()

    def handle_fetch_result(self, title, error):
        """处理获取网页标题的结果"""
        if error:
            self.text_output.append(error)
        else:
            self.text_output.append(f"网页标题: {title}\n")

        # 添加分隔线
        self.text_output.append("-" * 50)

    def cleanup_thread(self):
        """线程完成后的清理工作"""
        self.button1.setEnabled(True)  # 重新启用按钮
        self.fetch_thread = None

    def on_button2_click(self):
        self.input1.clear()
        self.input2.clear()
        self.text_output.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion样式，看起来更现代

    window = SimpleApp()
    window.show()
    sys.exit(app.exec_())
