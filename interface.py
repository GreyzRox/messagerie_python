import tkinter as tk
from tkinter import scrolledtext
from client import Client

class ChatInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Client Chat")

        # Zone de texte (affichage des messages)
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=20, state="disabled")
        self.text_area.pack(padx=10, pady=10)

        # Zone pour entrer le message
        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

        # Bouton envoyer
        self.send_button = tk.Button(self.root, text="Envoyer", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

        # Informations de connexion
        self.username = input("Nom d'utilisateur : ")
        self.server = input("Serveur : ")
        self.port = int(input("Port : "))

        # Création du client
        self.client = Client(self.username, self.server, self.port, self.display_message)
        self.client.listen()

        # Gestion de la fermeture
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def display_message(self, msg):
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, msg + "\n")
        self.text_area.yview(tk.END)
        self.text_area.config(state="disabled")

    def send_message(self):
        msg = self.entry.get()
        if msg:
            self.client.send(msg)
            self.entry.delete(0, tk.END)

    def on_close(self):
        self.client.send("QUIT")
        self.client.tidy_up()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ChatInterface()
    app.run()
