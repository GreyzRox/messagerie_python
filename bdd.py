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

    def getIdByUsername(self, user_name):
        self.cur.execute("SELECT * FROM utilisateur WHERE username = %s;", (user_name,))
        return self.cur.fetchone()
    
    def GetAllMessage(self):
        self.cur.execute("SELECT data,user_id FROM message;")
        return self.cur.fetchall()

    def getUserPswdById(self, user_id):
        self.cur.execute("SELECT password FROM utilisateur WHERE id = %s;", (user_id,))
        return self.cur.fetchone()
    
    def createUser(self, user_name, password):
        self.cur.execute("INSERT INTO utilisateur (user_id_seq.nextval(),username, password) VALUES (%s, %s);", (user_name, password))
        self.connection.commit()

    def getServerPswd(self):
        self.cur.execute("SELECT password FROM server;")
        return self.cur.fetchone()