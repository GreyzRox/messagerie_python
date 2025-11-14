import hashlib
import re
import socket
import threading
import time


class Client:
    def __init__(self, username, server, port, ui=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, port))
        self.username = username
        #self.send("USERNAME {0}".format(username))
        self.listening = True
        self.ui = ui

    def listener(self):
        while self.listening:
            data = ""
            try:
                data = self.socket.recv(1024).decode("UTF-8")
            except socket.error:
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1)

    def listen(self):
        self.listen_thread = threading.Thread(target=self.listener)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def send(self, message):
        try:
            username_result = re.search("^USERNAME (.*)$", message)
            if not username_result:
                message = "{0}:{1}".format(
                    self.username, message
                )
            self.socket.sendall(message.encode("UTF-8"))
        except socket.error:
            print("Unable to send message")

    def verif_password_user(self, username, pswd):
        # faire en sorte que le client envoie le mdp au serveur pour vérif puis écoute la réponse
        toSend = username + " " + pswd
        print("client: valeur qu'on envoie : " + toSend)
        try:
            self.socket.send(toSend.encode("UTF-8"))
        except socket.error:
            print("Unable to send password to server.")
        return self.listen_for_pswd_answer()

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

    def tidy_up(self):
        self.listening = False
        self.socket.close()

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
    username = input("username: ")
    server = input("server: ")
    port = int(input("port: "))
    pswd = hashlib.md5(b"" + input("mot de passe: ").encode()).hexdigest()

    client = Client(username=username, server=server, port=port)

    if client.verif_password_user(username, pswd):
        client.listen()
        message = ""
        while message != "QUIT":
            message = input()
            client.send(message)
            # print("\033[A\033[A")
    else:
        print("Password not")
