import socket # API qui permet de communiquer via des sockets
import threading # Module pour gérer les threads
import re # Module pour les expressions régulières
import time # Module pour faire des pauses (time.sleep)

# Classe pour gérer la communication avec un client
class ClientListener(threading.Thread):

    # Constructeur de la classe
    def __init__(self, server, socket, address):
        super(ClientListener, self).__init__()  # appel de la classe parent
        self.server = server 
        self.socket = socket
        self.address = address
        self.listening = True
        self.username = "No username"

    # Méthode principale du thread, qui sert à écouter les messages du client
    def run(self):

        msg = ""
        tmp = ""
        while True:
            try:
                tmp = self.socket.recv(1024).decode('UTF-8')
                print("tmp", tmp)
                msg += tmp
                if len(tmp) < 1024:
                    print(f"Valeur de msg : {msg}")
                    break
            except socket.error:
                print("Unable to receive username and password data from client")
                self.quit()
        
        login = msg.split()
        print("p1",login[0])
        print("p2",login[1])
        username = login[0]
        pswd = login[1]

        print(self.server.check_user_pswd(username,pswd))

        if not self.server(login[0], login[1]):
            self.socket.send('False'.encode('utf-8'))
            self.quit()
        self.socket.send('True'.encode('utf-8'))

        while self.listening:
            data = ""
            try:
                data = self.socket.recv(1024).decode('utf-8')
            except socket.error: # Gestion des erreurs de réception
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1) # Petite pause pour éviter de surcharger le CPU
        print("Ending client thread for", self.address)

    # Méthode pour gérer la déconnexion du client
    def quit(self):
        self.server.echo("{0} has quit \n".format(self.username))
        self.listening = False
        self.socket.close()
        self.server.remove_socket(self.socket)

    # Méthode pour traiter les messages reçus
    def handle_msg(self, data):
        print(self.address, " sent :", data)
        username_result = re.search(r"^USERNAME (.+)$", data) # Expression régulière pour extraire le nom d'utilisateur
        if username_result: # Si le message est un nom d'utilisateur
            self.username = username_result.group(1) # Récupération du nom d'utilisateur
            self.server.echo("{0} has joineeeeeeeeeeed \n".format(self.username)) # Annonce de la connexion du client
        elif data == "QUIT": # Si le message est une demande de déconnexion
            self.quit()
        elif data == "": # Si le message est vide, on considère que le client s'est déconnecté
            self.quit()
        else: # Sinon, on renvoie le message à tous les clients
            self.server.echo(data)