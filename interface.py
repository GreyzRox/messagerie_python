import hashlib
import tkinter as tk
from tkinter import scrolledtext, messagebox
from client import Client
from PIL import Image, ImageTk


class ChatInterface:
    #constructeur
    def __init__(self,client): 
        self.root = tk.Tk()
        self.root.title("Amber") #titre
        self.root.iconbitmap("logo_amber.ico") #icone
        self.root.configure(bg="#1a1a1a") #couleur du fond
        self.client = client #association du client
        self.root.state('zoomed') #fenetre en plein ecran

        # bibliotheque de couleurs
        dark_bg = "#1a1a1a"
        white = "#ffffff"
        input_bg = "#2d2d2d"
        sidebar_bg = "#242424"

        #creation de la fenetre de reception de message
        main_frame = tk.Frame(self.root, bg=dark_bg)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Modification de la fenetre de texte pour afficher les messages
        self.text_area = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            state="disabled",
            bg=dark_bg,
            fg=white,
            insertbackground=white,
            selectbackground=white,
            selectforeground=dark_bg,
            relief=tk.FLAT,
            font=("Segoe UI", 10)
        )
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # creation fenetre d'utilisateur connectés
        users_frame = tk.Frame(main_frame, width=220, bg=sidebar_bg)
        users_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        users_frame.pack_propagate(False)

        #modification fenetre utilisateur connectés
        tk.Label(
            users_frame, 
            text="Utilisateurs connectés", 
            bg=sidebar_bg, 
            fg=white,
            font=("Segoe UI", 12, "bold")
        ).pack(pady=15)

        # Liste des utilisateurs connectés
        self.users_listbox = tk.Listbox(
            users_frame, 
            bg=input_bg,
            fg=white,
            selectbackground=white,
            selectforeground=dark_bg,
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            highlightthickness=0
        )
        self.users_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Exemple d'utilisateurs connectés (à remplacer par les utilisateurs réels)
        example_users = ["Alice", "Bob", "Charlie", "David"]
        for user in example_users:
            self.users_listbox.insert(tk.END, user)

        # Frame pour l'entrée de message et le bouton d'envoi
        input_frame = tk.Frame(self.root, bg=dark_bg)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Modification de l'entrée de message
        self.entry = tk.Entry(
            input_frame,
            bg=input_bg,
            fg=white,
            insertbackground=white,
            relief=tk.FLAT,
            font=("Segoe UI", 11),
            highlightthickness=1,
            highlightbackground=white,
            highlightcolor=white
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)

        #modification du bouton d'envoi
        self.send_button = tk.Button(
            input_frame, 
            text="Envoyer",
            command=self.send_message,
            bg=white,
            fg=dark_bg,
            activebackground="#ff6b1a",
            activeforeground=white,
            relief=tk.FLAT,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            padx=20,
            pady=8
        )
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))
        self.entry.bind("<Return>", lambda event: self.send_message())

        # Gestion de la fermeture de la fenêtre
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # fonction pour afficher les messages dans la zone de texte
    def display_message(self, msg):
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, msg + "\n")
        self.text_area.yview(tk.END)
        self.text_area.config(state="disabled")
        self.text_area.config(fg="#ffffff")

    # fonction pour envoyer les messages
    def send_message(self):
        msg = self.entry.get()
        if msg:
            self.client.send(msg)
            self.entry.delete(0, tk.END)

    # gestion de la fermeture de la fenetre
    def on_close(self):
        self.client.send("QUIT")
        self.client.tidy_up()
        self.root.destroy()

    # fonction pour lancer la boucle principale de l'interface
    def run(self):
        self.root.mainloop()

# Classe de la fenetre de login
class LoginInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("420x150")

        # Création des champs de saisie
        # Champ user
        tk.Label(self.root, text="Username:").grid(row=0, column=0)
        self.user_entry = tk.Entry(self.root, width=50)
        self.user_entry.grid(row=0, column=1)

        #champ password
        tk.Label(self.root, text="Password:").grid(row=1, column=0)
        self.pswd_entry = tk.Entry(self.root, show="*", width=50)
        self.pswd_entry.grid(row=1, column=1)

        #champ server
        tk.Label(self.root, text="Server:").grid(row=2, column=0)
        self.server_entry = tk.Entry(self.root, width=50)
        self.server_entry.grid(row=2, column=1)

        #champ pswd
        tk.Label(self.root, text="Server Password:").grid(row=3, column=0)
        self.server_pswd_entry = tk.Entry(self.root, show="*", width=50)
        self.server_pswd_entry.grid(row=3, column=1)

        #champ port
        tk.Label(self.root, text="Port:").grid(row=4, column=0)
        self.port_entry = tk.Entry(self.root, width=50)
        self.port_entry.grid(row=4, column=1)

        #bouton de login
        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        #raccourci clavier 'Entrée' pour le login
        self.port_entry.bind("<Return>", lambda event: self.login())
        self.login_button.grid(row=5, column=1)

    # fonction de login 
    def login(self):
        #stockage des valeurs ecrit dans le champs
        username = self.user_entry.get()
        password = self.pswd_entry.get()
        server = self.server_entry.get()
        port_str = self.port_entry.get()
        
        #verification que tous les champs sont remplis
        if not username or not password or not server or not port_str:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        try:
            #conversion du port en entier et verification que le port est bien un int
            port = int(port_str)
        except ValueError:
            messagebox.showerror("Erreur", "Le port doit être un nombre entier")
            return
        
        #hachage du mot de passe avec md5
        pswd_hash = hashlib.md5(password.encode()).hexdigest()

        # Crée une connexion socket vers le serveur
        temp_client = Client(username, server, port)

        #verification du mot de passe avec le serveur
        if temp_client.verif_password_user(username, pswd_hash):
            self.root.destroy() #Ferme la fenêtre de login si le mdp est correct

            # On lance l'interface de chat
            chat_app = ChatInterface(temp_client)
            chat_app.client = temp_client
            chat_app.client.ui = chat_app.display_message
            chat_app.client.listen()
            chat_app.run()

        else:
            #msg d'erreur sinon
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")
            temp_client.tidy_up()



    def destroy(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    login_app = LoginInterface()
    login_app.run()