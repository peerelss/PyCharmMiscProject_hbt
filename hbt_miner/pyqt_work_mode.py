import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QCheckBox
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject, QThreadPool
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'Authorization': 'Digest username=root, realm=antMiner Configuration, nonce=5434d219f9cf57856d727bb10c608094, uri=/cgi-bin/stats.cgi, response=a24614ec7f918c96db70cd8ca0eccbaa, qop=auth, nc=0000004a, cnonce=0bb5916b63775c42',
    'Connection': 'keep-alive',
    'Referer': 'http://10.12.2.101/',
}



class Worker(QRunnable):
    # Worker class to run tasks in thread pool
    def __init__(self, ip, text_edit):
        super().__init__()
        self.ip = ip
        self.text_edit = text_edit

    def run(self):
        # 这里模拟处理每个ip的任务
        try:
            response = requests.get(f'http://{self.ip}/cgi-bin/stats.cgi', headers=headers)
            fans = (response.json()['STATS'][0]['fan'])
            self.text_edit.append(f"  {self.ip} fan: {fans}\n")
            print(self.ip, fans)
        except Exception as e:
            self.text_edit.append(f"❌ {self.ip} 错误: {e}\n")


class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.button = QPushButton('执行操作')
        self.button.clicked.connect(self.on_button_click)
        self.check_fan_button = QPushButton('查找风扇错误')
        self.check_fan_button.clicked.connect(self.check_fan_errors)

        self.switch = QCheckBox('正常模式')
        self.switch.setChecked(True)
        self.switch.stateChanged.connect(self.on_switch_toggle)

        self.textarea = QTextEdit()
        self.textarea.setPlaceholderText("请输入IP地址，每行一个，比如：\n10.11.1.1\n10.11.1.2")

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.check_fan_button)
        switch_layout = QHBoxLayout()
        switch_layout.addWidget(QLabel("模式切换："))
        switch_layout.addWidget(self.switch)
        layout.addLayout(switch_layout)

        layout.addWidget(self.textarea)

        self.setLayout(layout)
        self.setWindowTitle('矿机控制界面（POST版）')
        self.resize(800, 600)
        self.thread_pool = QThreadPool()

    def check_fan_errors(self):
        text = self.textarea.toPlainText()
        ip_list = [line.strip() for line in text.splitlines() if line.strip()]

        futures = []

        self.textarea.clear()  # 清空文本区域，准备展示最新结果

        for ip in ip_list:
            worker = Worker(ip, self.textarea)  # 创建 Worker 实例
            self.thread_pool.start(worker)  # 将任务提交给线程池

        self.textarea.append("🔧 风扇错误检查完成。\n")

    def fan_miss(self, ip):
        try:
            response = requests.get(f'http://{ip}/cgi-bin/stats.cgi', headers=headers)
            fans = (response.json()['STATS'][0]['fan'])
            print(ip, fans)
            return [ip, fans]
        except Exception as e:
            print(f" {ip}: {e}")
            return [ip, e]

    def on_button_click(self):
        text = self.textarea.toPlainText()
        ip_list = [line.strip() for line in text.splitlines() if line.strip()]

        if not ip_list:
            print("没有有效IP地址")
            return

        if self.switch.isChecked():
            mode = 0  # 正常模式
        else:
            mode = 1  # 休眠模式

        print(f"当前切换模式：{'正常' if mode == 0 else '休眠'}")
        print(f"准备并发请求 {len(ip_list)} 个矿机...")

        futures = []
        for ip in ip_list:
            futures.append(self.thread_pool.submit(self.send_command, ip, mode))

        for future in as_completed(futures):
            result = future.result()
            print(result)

    def send_command(self, ip, mode):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Origin': 'http://10.102.1.143',
            'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="68695f7e82979e8636957c0788c7cb19", uri="/cgi-bin/set_miner_conf.cgi", response="a954bf4eff410b6eb0ffb26f4a866c66", qop=auth, nc=00000041, cnonce="0664436edfd7834f"',
            'Connection': 'keep-alive',
            'Referer': 'http://10.102.1.143/',
            'Priority': 'u=0',
        }

        data = '{"bitmain-fan-ctrl":false,"bitmain-fan-pwm":"100","bitmain-hashrate-percent":"100","miner-mode":0,"freq-level":"100","pools":[{"url":"stratum+tcp://ss.antpool.com:3333","user":"AMTX22.10x41x10x230","pass":"root"},{"url":"stratum+tcp://ss.antpool.com:443","user":"AMTX22.10x41x10x230","pass":"root"},{"url":"stratum+tcp://btc.f2pool.com:1314","user":"amtx22f2pool.10x41x10x230","pass":"root"}]}'
        if mode == 1:
            data = '{"bitmain-fan-ctrl":false,"bitmain-fan-pwm":"100","bitmain-hashrate-percent":"100","miner-mode":1,"freq-level":"100","pools":[{"url":"stratum+tcp://ss.antpool.com:3333","user":"AMTX22.10x41x10x230","pass":"root"},{"url":"stratum+tcp://ss.antpool.com:443","user":"AMTX22.10x41x10x230","pass":"root"},{"url":"stratum+tcp://btc.f2pool.com:1314","user":"amtx22f2pool.10x41x10x230","pass":"root"}]}'
        try:
            response = requests.post(f'http://{ip}/cgi-bin/set_miner_conf.cgi', headers=headers, data=data)
            print(ip, response.json())
            if response.status_code == 200:
                return f"{ip} 设置 {('正常' if mode == 0 else '休眠')} 成功"
            else:
                return f"{ip} 设置失败，状态码：{response.status_code}"

        except Exception as e:
            return f"{ip} 请求出错：{e}"

    def on_switch_toggle(self):
        if self.switch.isChecked():
            self.switch.setText('正常模式')
        else:
            self.switch.setText('休眠模式')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec_())
