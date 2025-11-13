import hashlib
import json
import socket  # API qui permet de communiquer via des sockets
import sys  # utilisé pour sortir du programme
import time  # Module pour faire des pauses (time.sleep)
from json.decoder import JSONDecodeError

from bdd import DB
from clientthread import ClientListener


class Server:
    def __init__(self, port):  # Constructeur de la class 'Server'
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(("", port))
        self.listener.listen(1)
        print("Listening on port ", port)
        self.clients_sockets = []
        # self.cursor = DB()
        file = open("data.json")
        self.db = json.load(file)
        file.close()

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
            time.sleep(0.1)
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

    def check_user_pswd(self, username, pswd):
        user_id = (((self.db["amber_db"])["utilisateurs"])[0])["id"]  # remplacer par une boucle qui trouve le bon user
        user_pswd = (((self.db["amber_db"])["utilisateurs"])[0])["password"] # pareil ici

        print("print dans 'check_user_pswd' de server.py")

        if user_pswd == pswd:
            return True
        else:
            return False
        
    def check_server_pswd(self, pswd):
        server_pswd = (((self.db["amber_db"])["serveur"])[0])["password"] # récupère le mdp du serveur depuis le json et le hash
        return pswd == hashlib.md5(b"" + server_pswd.encode()).hexdigest()


if __name__ == "__main__":
    pswd = hashlib.md5(b"" + input("mot de passe: ").encode()).hexdigest()
    server = Server(59001)
    if server.check_server_pswd(pswd):
        server.run()
    else:
        sys.exit("Wrong server password.")
