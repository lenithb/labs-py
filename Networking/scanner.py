import socket
import sys
from concurrent.futures import ThreadPoolExecutor

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            print(f"[+] {port}/tcp  abierto")
    except:
        pass

def main():
    if len(sys.argv) < 2:
        print(f"Uso: python3 {sys.argv[0]} <host> [port_inicio] [port_fin]")
        sys.exit(1)

    host = sys.argv[1]
    port_start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    port_end = int(sys.argv[3]) if len(sys.argv) > 3 else 1024

    print(f"[*] Escaneando {host} — puertos {port_start} a {port_end}")

    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(port_start, port_end + 1):
            executor.submit(scan_port, host, port)

    print("[*] Escaneo completo")

if __name__ == "__main__":
    main()