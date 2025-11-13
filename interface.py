import tkinter as tk
from tkinter import scrolledtext
from client import Client


class ChatInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Amber")
        self.root.geometry("1080x720")

        # Zone des affichage des messages
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=150, height=20, state="disabled")
        self.text_area.pack(padx=10, pady=10)

        # Zone pour entrer le message
        self.entry = tk.Entry(self.root, width=100)
        self.entry.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Bouton envoyer
        self.send_button = tk.Button(self.root, text="Envoyer", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

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

class LoginInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("420x150")

        tk.Label(self.root, text="Username:").grid(row=0, column=0)
        self.user_entry = tk.Entry(self.root,width=50).grid(row=0, column=1)

        tk.Label(self.root, text="Password:").grid(row=1, column=0)
        self.pswd_entry = tk.Entry(self.root, show="*", width=50).grid(row=1, column=1)

        tk.Label(self.root, text="Server:").grid(row=2, column=0)
        self.server_entry = tk.Entry(self.root, width=50).grid(row=2, column=1)

        tk.Label(self.root, text="Server Password:").grid(row=3, column=0)
        self.server_pswd_entry = tk.Entry(self.root, show="*", width=50).grid(row=3, column=1)

        tk.Label(self.root, text="Port:").grid(row=4, column=0)
        self.port_entry = tk.Entry(self.root, width=50).grid(row=4, column=1)

        self.login_button = tk.Button(self.root, text="Login")
        self.login_button.grid(row=5, column=1)

        if self.login_button:
            chatInterface = ChatInterface()
            chatInterface.run()


    def destroy(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    login_app = LoginInterface()
    login_app.run()