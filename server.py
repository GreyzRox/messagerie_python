import socket # API qui permet de communiquer via des sockets
import sys # utilisé pour sortir du programme
import time # Module pour faire des pauses (time.sleep)
from clientthread import ClientListener
import hashlib
from bdd import DB



class Server():

    def __init__(self, port): # Constructeur de la class 'Server'
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        print("Listening on port ", port)
        self.clients_sockets=[]
        self.cursor = DB()
        self.liste_user = []

    def verif_password(self, pswd):
        password = self.cursor.getServerPswd()
        (a,) = password
        if(pswd == a):
            return True
        else:
            return False

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

    def check_user_pswd(self, username, pswd):
        user_data = self.cursor.getIdByUsername(username)
        if not user_data:
            return False
        
        user_id = user_data[0]
        user_pswd_result = self.cursor.getUserPswdById(user_id)        
        if user_pswd_result and user_pswd_result[0] == pswd:
            return True
        else:
            return False
        
    def send_user_all(self):
        for sock in self.clients_sockets:
            for usr in self.liste_user:
                try:
                    sock.sendall(usr.encode("UTF-8") + b"\n")
                except socket.error:
                    print("Cannot send the message")

if __name__ == "__main__":
    pswd = hashlib.md5(b'' + input("mot de passe: ").encode()).hexdigest()
    server = Server(59001)
    if server.verif_password(pswd=pswd):
        server.run()
    else:
        print("Wrong server password.")