# listener.py
import socket

port = 14235
buffer_size = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 监听所有IP上的14235端口
sock.bind(('', port))
print(f"Listening on UDP port {port}...")

try:
    while True:
        data, addr = sock.recvfrom(buffer_size)
        print(f"Received from {addr}: {data}")
except KeyboardInterrupt:
    print("Listener stopped.")
finally:
    sock.close()
