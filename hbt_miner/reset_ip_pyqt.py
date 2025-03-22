import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QCheckBox

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
    app = QApplication(sys.argv)
    ex = MinerConfigApp()
    ex.show()
    sys.exit(app.exec_())