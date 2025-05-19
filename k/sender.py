# sender.py
import socket
import time

broadcast_ip = '192.168.39.255'
port = 14235
message = b'Hello from sender!'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

try:
    for i in range(0, 5):
        sock.sendto(message, (broadcast_ip, port))
        print(f"Sent: {message}")
        time.sleep(2)
except KeyboardInterrupt:
    print("Sender stopped.")
finally:
    sock.close()
