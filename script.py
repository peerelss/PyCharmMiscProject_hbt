import subprocess
import platform

def is_ip_online(ip):
    # 根据系统选择 ping 命令
    if platform.system().lower() == "windows":
        cmd = ["ping", "-n", "1", "-w", "1000", ip]  # Windows
    else:
        cmd = ["ping", "-c", "1", "-W", "1", ip]  # Linux/macOS

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0  # returncode == 0 表示成功
    except Exception as e:
        print(f"Error: {e}")
        return False

# 测试 IP
ip_address = "10.91.1.1"
if is_ip_online(ip_address):
    print(f"IP {ip_address} 在线")
else:
    print(f"IP {ip_address} 离线")
