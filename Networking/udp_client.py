import socket
import sys

host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"[*] Enviando a {host}:{port} — Ctrl+C para salir")

while True:
    msg = input(">> ")
    sock.sendto(msg.encode(), (host, port))
    data, _ = sock.recvfrom(4096)
    print(f"[server] {data.decode()}")