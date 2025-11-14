import hashlib
import tkinter as tk
from tkinter import scrolledtext, messagebox
from client import Client


class ChatInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Amber")
        self.root.state('zoomed')
        self.root.configure(bg="#1a1a1a")

        dark_bg = "#1a1a1a"
        orange = "#ffffff"
        white = "#ffffff"
        input_bg = "#2d2d2d"
        sidebar_bg = "#242424"

        main_frame = tk.Frame(self.root, bg=dark_bg)
        main_frame = tk.Frame(self.root, bg=dark_bg)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.text_area = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            state="disabled",
            bg=dark_bg,
            fg=white,
            insertbackground=orange,
            selectbackground=orange,
            selectforeground=dark_bg,
            relief=tk.FLAT,
            font=("Segoe UI", 10)
        )
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        users_frame = tk.Frame(main_frame, width=220, bg=sidebar_bg)
        users_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        users_frame.pack_propagate(False)

        tk.Label(
            users_frame, 
            text="Utilisateurs connectés", 
            bg=sidebar_bg, 
            fg=orange,
            font=("Segoe UI", 12, "bold")
        ).pack(pady=15)

        self.users_listbox = tk.Listbox(
            users_frame, 
            bg=input_bg,
            fg=white,
            selectbackground=orange,
            selectforeground=dark_bg,
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            highlightthickness=0
        )
        self.users_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        example_users = ["Alice", "Bob", "Charlie", "David"]
        for user in example_users:
            self.users_listbox.insert(tk.END, user)

        input_frame = tk.Frame(self.root, bg=dark_bg)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.entry = tk.Entry(
            input_frame,
            bg=input_bg,
            fg=white,
            insertbackground=orange,
            relief=tk.FLAT,
            font=("Segoe UI", 11),
            highlightthickness=1,
            highlightbackground=orange,
            highlightcolor=orange
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)

        self.send_button = tk.Button(
            input_frame, 
            text="Envoyer",
            command=self.send_message,
            bg=orange,
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
        self.user_entry = tk.Entry(self.root, width=50)
        self.user_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Password:").grid(row=1, column=0)
        self.pswd_entry = tk.Entry(self.root, show="*", width=50)
        self.pswd_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Server:").grid(row=2, column=0)
        self.server_entry = tk.Entry(self.root, width=50)
        self.server_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Server Password:").grid(row=3, column=0)
        self.server_pswd_entry = tk.Entry(self.root, show="*", width=50)
        self.server_pswd_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Port:").grid(row=4, column=0)
        self.port_entry = tk.Entry(self.root, width=50)
        self.port_entry.grid(row=4, column=1)

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.grid(row=5, column=1)

    def login(self):
        username = self.user_entry.get()
        password = self.pswd_entry.get()
        server = self.server_entry.get()
        port_str = self.port_entry.get()
        
        if not username or not password or not server or not port_str:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        try:
            port = int(port_str)
        except ValueError:
            messagebox.showerror("Erreur", "Le port doit être un nombre entier")
            return
        
        pswd_hash = hashlib.md5(password.encode()).hexdigest()

        temp_client = Client(username, server, port)

        if temp_client.verif_password_user(username, pswd_hash):
            self.root.destroy()

            chat_app = ChatInterface(temp_client)
            chat_app.run()

        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")
            temp_client.tidy_up()



    def destroy(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    login_app = LoginInterface()
    login_app.run()