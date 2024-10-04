from tkinter import *
import secrets
import string
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["password_manager"]
collection = db["password_manager"]

USER_CREDENTIALS = {
    "example": "test" 
}

def store_passwords(passwords):
    for idx, passwd in enumerate(passwords):
        collection.insert_one({"password_id": idx + 1, "password": passwd})

def show_password_generator():
    # Password Generator Window
    generator_window = Toplevel(root)
    generator_window.title("Random Password Generator")

    # Labels for input fields
    passwordNum = Label(generator_window, text='Please enter desired number of passwords')
    passwordLen = Label(generator_window, text='Please enter character length (min 8)')
    
    # Position the labels on the grid
    passwordNum.grid(column=0, row=0)
    passwordLen.grid(column=0, row=3)
    
    # Spinbox for user inputs
    spin = Spinbox(generator_window, from_=1, to=25, width=5)
    spin1 = Spinbox(generator_window, from_=8, to=25, width=5)  
    
    # Position the spinboxes on the grid
    spin.grid(column=0, row=1)
    spin1.grid(column=0, row=4)
    
    # Character set for password generation
    chars = string.ascii_letters + string.digits + string.punctuation
    
    def clicked():
        t.delete('1.0', END)  # Clear the text area
        num_passwords = int(spin.get())
        password_length = int(spin1.get())
        
        passwords = []
        for i in range(num_passwords):
            passwd = ''.join(secrets.choice(chars) for _ in range(password_length))
            passwords.append(passwd)
            t.insert(INSERT, f"Password {i + 1}: {passwd}\n")
        
        # Store passwords in MongoDB
        store_passwords(passwords)
    
    # Generate button
    btn = Button(generator_window, text='Generate', command=clicked)
    btn.grid(column=0, row=5)
    
    # Text area to display generated passwords
    t = Text(generator_window, height=18, width=55)
    t.grid(column=0, row=7)

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if USER_CREDENTIALS.get(username) == password:
        login_window.destroy()
        show_password_generator()
    else:
        login_error_label.config(text="Invalid username or password")

# Main window for login
root = Tk()
root.title("Login")

login_window = Frame(root)
login_window.pack(padx=10, pady=10)

# Login labels and entries
username_label = Label(login_window, text="Username:")
username_label.grid(column=0, row=0, pady=5)
username_entry = Entry(login_window)
username_entry.grid(column=1, row=0, pady=5)

password_label = Label(login_window, text="Password:")
password_label.grid(column=0, row=1, pady=5)
password_entry = Entry(login_window, show="*")
password_entry.grid(column=1, row=1, pady=5)

login_error_label = Label(login_window, text="", fg="red")
login_error_label.grid(column=0, row=2, columnspan=2)

login_button = Button(login_window, text="Login", command=login)
login_button.grid(column=0, row=3, columnspan=2, pady=10)

root.mainloop()

