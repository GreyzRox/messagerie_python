import socket # API qui permet de communiquer via des sockets
import threading # Module pour gérer les threads
import re # Module pour les expressions régulières
import time # Module pour faire des pauses (time.sleep)

class ClientListener(threading.Thread): # Classe pour gérer la communication avec un client

    def __init__(self, server, socket, address): # Constructeur de la classe
        super(ClientListener, self).__init__()  # appel de la classe parent
        self.server = server 
        self.socket = socket
        self.address = address
        self.listening = True
        self.username = "No username"

    def run(self): # Méthode principale du thread, qui sert à écouter les messages du client
        while self.listening:
            data = ""
            try:
                data = self.socket.recv(1024).decode('utf-8')
            except socket.error: # Gestion des erreurs de réception
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1) # Petite pause pour éviter de surcharger le CPU
        print("Ending client thread for", self.address)

    def quit(self): # Méthode pour gérer la déconnexion du client
        self.server.echo("{0} has quit \n".format(self.username))
        self.listening = False
        self.socket.close()
        self.server.remove_socket(self.socket)

    def handle_msg(self, data): # Méthode pour traiter les messages reçus
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