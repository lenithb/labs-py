import socket
import threading

connections = []
total_connections = 0

class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)

def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[-1].start()
        print("New connection at ID " + str(connections[-1].id) + " " + str(address))
        total_connections += 1

def main():
    host = input("Host: ")
    port = int(input("Port: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    
    # Inicia el hilo para aceptar nuevas conexiones
    threading.Thread(target=newConnections, args=(sock,)).start()

if __name__ == "__main__":
    main()