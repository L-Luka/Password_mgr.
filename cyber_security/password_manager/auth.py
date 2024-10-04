import getpass
from password_manager.storage import initialize_db, store_master_key, retrieve_passwords
from password_manager.encryption import generate_symmetric_key, generate_rsa_keys, serialize_private_key, serialize_public_key, encrypt_with_public_key, decrypt_with_private_key

def create_user(username, master_password):
    salt = b'some_random_salt'  # In production, use a secure random generator for salt
    master_key = generate_symmetric_key(master_password, salt)
    private_key, public_key = generate_rsa_keys()
    encrypted_master_key = encrypt_with_public_key(public_key, master_key)
    store_master_key(username, encrypted_master_key)
    with open(f"{username}_private_key.pem", "wb") as key_file:
        key_file.write(serialize_private_key(private_key))
    with open(f"{username}_public_key.pem", "wb") as key_file:
        key_file.write(serialize_public_key(public_key))
    print("User created successfully.")

def login(username):
    master_password = getpass.getpass(prompt="Enter master password: ")
    salt = b'some_random_salt'
    master_key = generate_symmetric_key(master_password, salt)
    try:
        with open(f"{username}_private_key.pem", "rb") as key_file:
            private_key = load_private_key(key_file.read())
        encrypted_master_key = retrieve_master_key(username)
        decrypted_master_key = decrypt_with_private_key(private_key, encrypted_master_key)
        if master_key == decrypted_master_key:
            print("Login successful.")
            return master_key
        else:
            print("Invalid master password.")
            return None
    except Exception as e:
        print(f"Login failed: {e}")
        return None
