import getpass
from password_manager.auth import create_user, login
from password_manager.storage import store_password, retrieve_passwords

def main_menu():
    print("Password Manager")
    print("1. Create User")
    print("2. Login")
    print("3. Exit")
    choice = input("Choose an option: ")
    return choice

def create_user_ui():
    username = input("Enter username: ")
    master_password = getpass.getpass(prompt="Enter master password: ")
    create_user(username, master_password)

def login_ui():
    username = input("Enter username: ")
    key = login(username)
    if key:
        while True:
            print("\nPassword Manager")
            print("1. Store Password")
            print("2. Retrieve Passwords")
            print("3. Logout")
            choice = input("Choose an option: ")
            if choice == "1":
                name = input("Enter password name: ")
                user = input("Enter username: ")
                pwd = getpass.getpass(prompt="Enter password: ")
                store_password(username, name, user, pwd, key)
                print("Password stored successfully.")
            elif choice == "2":
                passwords = retrieve_passwords(username, key)
                for name, user, pwd in passwords:
                    print(f"\nName: {name}\nUsername: {user}\nPassword: {pwd}")
            elif choice == "3":
                break
            else:
                print("Invalid option.")

def run_ui():
    initialize_db()
    while True:
        choice = main_menu()
        if choice == "1":
            create_user_ui()
        elif choice == "2":
            login_ui()
        elif choice == "3":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    run_ui()
