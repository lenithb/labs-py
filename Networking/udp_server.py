import socket
import sys

host = "0.0.0.0"
port = int(sys.argv[1]) if len(sys.argv) > 1 else 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))
print(f"[*] Escuchando en {host}:{port}")

while True:
    data, addr = sock.recvfrom(4096)
    print(f"[{addr[0]}:{addr[1]}] {data.decode()}")
    sock.sendto(b"OK", addr)