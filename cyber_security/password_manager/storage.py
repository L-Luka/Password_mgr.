import sqlite3
import os
from password_manager.encryption import encrypt_data, decrypt_data, generate_symmetric_key

DATABASE = "password_manager"
SALT = b' ######' 

def initialize_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE users (username TEXT PRIMARY KEY, master_key BLOB)''')
        c.execute('''CREATE TABLE passwords (id INTEGER PRIMARY KEY, user TEXT, name TEXT, username TEXT, password BLOB, FOREIGN KEY(user) REFERENCES users(username))''')
        conn.commit()
        conn.close()

def store_master_key(username, master_key):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, master_key) VALUES (?, ?)", (username, master_key))
    conn.commit()
    conn.close()

def store_password(username, name, user, pwd, key):
    encrypted_password = encrypt_data(key, pwd)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO passwords (user, name, username, password) VALUES (?, ?, ?, ?)", (username, name, user, encrypted_password))
    conn.commit()
    conn.close()

def retrieve_passwords(username, key):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT name, username, password FROM passwords WHERE user=?", (username,))
    rows = c.fetchall()
    decrypted_passwords = [(name, user, decrypt_data(key, pwd)) for (name, user, pwd) in rows]
    conn.close()
    return decrypted_passwords
