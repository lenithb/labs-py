import socket
import threading
import sys

def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("Estas desconectado del servidor")
            signal = False
            break

host = input("Host: ")
port = int(input("Port: "))

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except:
    print("No podes conectarte al servidor")
    input("Presiona Enter para salir")
    sys.exit(0)

receiveThread = threading.Thread(target=receive, args=(sock, True))
receiveThread.start()

while True:
    message = input()
    sock.sendall(str.encode(message))