import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

results = []

def grab_banner(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()
        if banner:
            print(f"[+] {port}/tcp — {banner[:80]}")
            results.append((port, banner))
    except:
        pass

def save_results(host):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"banners_{host.replace('.', '_')}_{timestamp}.txt"
    with open(filename, "w") as f:
        for port, banner in results:
            f.write(f"[{port}]\n{banner}\n\n")
    print(f"[*] Resultado guardado en {filename}")

def main():
    if len(sys.argv) < 2:
        print(f"Uso: python3 {sys.argv[0]} <host> [port_inicio] [port_fin]")
        print(f"Ejemplo: python3 {sys.argv[0]} 10.10.10.1 1 1024")
        sys.exit(1)

    host = sys.argv[1]
    port_start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    port_end = int(sys.argv[3]) if len(sys.argv) > 3 else 1024

    print(f"[*] Grabbing banners en {host} — puertos {port_start} a {port_end}")

    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(port_start, port_end + 1):
            executor.submit(grab_banner, host, port)

    print(f"\n[*] {len(results)} banners capturados")
    if results:
        save_results(host)

if __name__ == "__main__":
    main()