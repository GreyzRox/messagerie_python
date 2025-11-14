import hashlib
import re
import socket
import threading
import time


class Client:

    #Constructeur
    def __init__(self, username, server, port, ui=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, port))
        self.username = username
        self.listening = True
        self.ui = ui

    #Fonction qui permet d'écouter l'entrée des messages
    def listener(self):
        while self.listening:
            data = ""
            try:
                data = self.socket.recv(1024).decode("UTF-8")
            except socket.error:
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1)

    #Fonction qui démarre l'écoute sur les messages
    def listen(self):
        self.listen_thread = threading.Thread(target=self.listener)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    #Fonction qui permet d'envoyer les messages à tous les utilisateurs
    def send(self, message):
        try:
            username_result = re.search("^USERNAME (.*)$", message)
            if not username_result:
                message = "{0}:{1}\n".format(
                    self.username, message
                )
            self.socket.sendall(message.encode("UTF-8"))
        except socket.error:
            print("Unable to send message")

    #Fonction qui permet au client d'envoyer le mdp au serveur pour vérif puis écoute la réponse
    def verif_password_user(self, username, pswd):
        toSend = username + " " + pswd
        print("client: valeur qu'on envoie : " + toSend)
        try:
            self.socket.send(toSend.encode("UTF-8"))
        except socket.error:
            print("Unable to send password to server.")
        return self.listen_for_pswd_answer()

    #Fonction qui écoute la réponse du server pour le mot de passe
    def listen_for_pswd_answer(self):
        data = ""
        try:
            data = self.socket.recv(1024).decode("UTF-8")
        except socket.error:
            print("Unable to receive data")
        if data == "True":
            return True
        else:
            return False

    #Fonction qui permet de fermer le socket
    def tidy_up(self):
        self.listening = False
        self.socket.close()

    #Fonction qui permet de vérifier le contenu du message
    def handle_msg(self, data):
        if data == "QUIT":
            self.tidy_up()
        elif data == "":
            self.tidy_up()
        else:
            if self.ui:
                self.ui(data)
            print(data)        


if __name__ == "__main__":
    #Entrée utilisateur
    username = input("username: ")
    server = input("server: ")
    port = int(input("port: "))
    pswd = hashlib.md5(b"" + input("mot de passe: ").encode()).hexdigest()

    client = Client(username=username, server=server, port=port)

    #Vérification de la connexion de l'utilisateur
    if client.verif_password_user(username, pswd):
        client.listen()
        message = ""
        while message != "QUIT":
            message = input()
            client.send(message)
    else:
        print("Password not")
