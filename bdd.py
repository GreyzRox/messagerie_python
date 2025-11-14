import psycopg2
import os
from dotenv import load_dotenv, dotenv_values 


class DB:

    def __init__(self):
        self.connection = self.connect_to_db()
        self.cur = self.connection.cursor()

    def connect_to_db(self):
        connection = psycopg2.connect(
            dbname=dotenv_values(".env")["DB_NAME"],
            user=dotenv_values(".env")["DB_USER"],
            password=dotenv_values(".env")["DB_PSWD"],
            port = dotenv_values(".env")["DB_PORT"],
        )
        return connection

    def getIdByUsername(self, user_name): #Fonction qui permet de récupérer le nom d'utilisateur avec l'Id
        self.cur.execute("SELECT id FROM utilisateur WHERE username = %s;", (user_name,))
        return self.cur.fetchone()

    def getUserPswdById(self, user_id): #Fonction qui permet de récupérer le mot de passe avec l'Id
        self.cur.execute("SELECT password FROM utilisateur WHERE id = %s;", (user_id,))
        return self.cur.fetchone()

    def getServerPswd(self): #Fonction qui permet de récupérer le mot de passe du serveur
        self.cur.execute("SELECT password FROM server;")
        return self.cur.fetchone()
    
    def insertMessageIntoDB(self, message, user_id): #Fonction qui permet d'insérer les messages dans la BD
        self.cur.execute("INSERT INTO message VALUES (nextval('message_id_seq'), %s, %s);", (message, user_id))
        self.connection.commit()

    def getMessages(self): #Fonction qui permet de récupérer tous les messages
        self.cur.execute("SELECT data FROM message;")
        return self.cur.fetchall()