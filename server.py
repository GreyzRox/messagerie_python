import socket # API qui permet de communiquer via des sockets
import sys # utilisé pour sortir du programme
import time # Module pour faire des pauses (time.sleep)
from clientthread import ClientListener

class Server():

    def __init__(self, port): # Constructeur de la class 'Server'
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        print("Listening on port ", port)
        self.clients_sockets=[]

    def run(self):
        while True:
            print("Listening new customers")
            try:
                (client_socket, client_adress) = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
            self.clients_sockets.append(client_socket)
            print("Start the thread for client : ", client_adress)
            client_thread = ClientListener(self, client_socket, client_adress)
            client_thread.start()
            time.sleep(0.1)

    def remove_socket(self, socket):
        self.clients_sockets.remove(socket)

    def echo(self, data):
        print("echoing : ", data)
        for sock in self.clients_sockets:
            try:
                sock.sendall(data.encode("UTF-8"))
            except socket.error:
                print("Cannot send the message")

if __name__ == "__main__":
    server = Server(59001)
    server.run()