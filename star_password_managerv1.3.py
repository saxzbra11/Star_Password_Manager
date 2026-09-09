
#This is the code for Star Password Manager, if you're reading this, in this code you'll find a bunch of comments that explain how the program works.
#You can modify it, but publish it on the development-test branch on github so the developer can see the changes
#WARNING: This program is open source and free to use, don't commercalize it or sell it without the author's permission. To contact the author, ask question on the contact on the github repo

#STAR PASSWORD MANAGER V1.3
#-----------------------------------------------------------

#Import list
import os
import base64
import hashlib
from getpass import getpass
from cryptography.fernet import Fernet
import secrets
import json
import hmac

#-----------------------------------------------------------
#MASTER PASSWORD PART

#Master password variables with sha256 cryptography
MASTER_FILE = "master.json"
ITERATIONS = 200_000
HASH_ALGO = "sha256"
SALT_BYTES = 16

#Derive hash function (for master pasword), the password is generated with SALT_BYTES variable and the hash is generated with the hashlib.
def _deriva_hash(password, salt):
    return hashlib.pbkdf2_hmac(HASH_ALGO, password.encode("utf-8"), salt, ITERATIONS)
 
 #Master password CREATION
def crea_master_password():
    print("Welcome! You need to create a master password to protect your passwords (Don't forget it after creating it!).")
    while True:
        pwd1 = getpass("Create a master password: ")
        pwd2 = getpass("Confirm the master password: ")
        if pwd1 == pwd2:
            break
        print("The passwords do not match. Please try again.\n")

    salt = secrets.token_bytes(SALT_BYTES)
    pwd_hash = _deriva_hash(pwd1, salt)

    dati = {"salt": salt.hex(), "hash": pwd_hash.hex()}
    with open(MASTER_FILE, "w") as f:
        json.dump(dati, f)

    print("Master password created and saved successfully. Have Fun using the program!\n")

    key = key_cryptography(pwd1, salt)
    return create_fernet(key)

#Master password VERIFICATION
def verificate_master_password():
    with open(MASTER_FILE, "r") as f:
        dati = json.load(f)

# Load the stored salt and expected hash from the data file (hex -> bytes)
    salt = bytes.fromhex(dati["salt"])
    hash_salvato = bytes.fromhex(dati["hash"])
# getpass hides input so the password isn't echoed to the terminal/logs
    while True:
        pwd = getpass("Enter the master password: ")
        hash_calcolato = _deriva_hash(pwd, salt)
#Use constant-time comparison to prevent timing attacks 
        if hmac.compare_digest(hash_calcolato, hash_salvato):
            print("Access granted.\n")
# Derive the actual encryption key from the verified password
            key = key_cryptography(pwd, salt)
            return create_fernet(key)
        print("Password incorrect, try again.\n")

#-----------------------------------------------------------
# Little secret, def variable to hide the json and .txt files in the APPDATA folder :D (ONLY ON WINDOWS) -i spent too much hours finding this and implement it, so pleeease don't touch it!
#The json and txt can be found in the %APPDATA% folder on windows

def get_data_dir():
    if os.name == "nt":  # Windows save
        base = os.getenv("APPDATA")
    else:  # Linux/Mac save
        base = os.path.expanduser("~/.config")
    data_dir = os.path.join(base, "StarPasswordManager")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

MASTER_FILE = os.path.join(get_data_dir(), "master.json")
PASSWORD_FILE = os.path.join(get_data_dir(), "password.txt")
#-----------------------------------------------------------

#FERNET ENCRYPTION AND DECRYPTION PART (finally) based on AES 128 and sha256

#Fernet encryption and decryption, the passwords will be saved on a .txt file with the name of the service and the encrypted password, it will decrypt the password when you search for it in the program.
def cifra(testo, fernet):
    return fernet.encrypt(testo.encode()).decode()

def decifra(testo, fernet):
    return fernet.decrypt(testo.encode()).decode()
#-----------------------------------------------------------
#FUNCTIONS TO SAVE,DELETE AND VIEW PASSWORDS (the delete password function is in the next part of the code, i guess if it works i'll leave it here -if it works,don't touch it- :D)

# Save password function
def save_password(fernet):
    nome = input("Enter the name of the application: ")
    password = input("Enter the password: ")
    password_cifrata = cifra(password, fernet)
    with open(PASSWORD_FILE, "a") as file:
        file.write(nome + ":" + password_cifrata + "\n")
    print("The password has been saved!")

def view_password(fernet):
    nome = input("Enter the name of the application to search for: ")
    if os.path.exists(PASSWORD_FILE):
        trovato = False
        with open(PASSWORD_FILE, "r") as file:
            for line in file:
                if line.startswith(nome + ":"):
                    parti = line.split(":", 1)
                    print("The password is: " + decifra(parti[1].strip(), fernet))
                    trovato = True
                    break
        if not trovato:
            print("No password found for this name.")
    else:
        print("There are no passwords saved yet.")

# List services function
def lista_servizi():
     if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            servizi = [line.split(":", 1)[0] for line in file if line.strip()]
        if servizi:
            print("Servizi salvati:")
            for servizio in servizi:
                print("- " + servizio)
#-----------------------------------------------------------
# PASSWORD CRYPTION AND DECRYPTION WITH FERNET

# Cryptography key generation function
def key_cryptography(password, salt):
    key_raw = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS, dklen=32)
    return base64.urlsafe_b64encode(key_raw)

# Fernet object creation function
def create_fernet(key):
    return Fernet(key)

#-----------------------------------------------------------
    
#ASCII art

ASCII_ART = r"""
⠀⠀⠀⠀⠀     ⢀⣤⣤⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠋⠀⠀⠙⢿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⠀⠀⠀⠀⠀⠙⢿⣦⡀⠀⠀⢀⣀⣀⣠⣤⣀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠙⠿⠿⠟⠛⠛⠋⠉⠉⠛⣷⡄
⠀⠀⠀⠀⠀⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⠀⠀⠀⠀⣀⣤⣶⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠃
⠀⣠⣶⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡿⠣⠀
⢸⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠁⠀⠀
⢸⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⡀⠄⠀
⠀⠙⠿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⡄⠀
⠀⠀⠀⠀⠉⠛⠿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡄
⠀⠀⠀⠀⠀⠀⠀⠘⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⠀⠀⠀⠀⠀⠀⠀⠀⣿⡆⠀⠀⠀⠀⠀⠀⠀⣠⣶⣶⣦⣤⣤⣄⣀⣀⣤⡿⠃
⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠀⠀⠀⠀⠀⣠⣾⠏⠀⠀⠀⠈⠉⠉⠙⠛⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣄⠀⠀⣠⣾⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠛⠛⠁⠀⠀
"""
#-----------------------------------------------------------
#INPUT AND OUTPUT PART (it's the "front end" of the program, where you can choose to save,delete,view a password by name or view a list of all the services you saved in the program.)

#STARTING of the program with the ascii and a welcome message

def main(fernet):
    print("*****************************************")
    print("    STAR PASSWORD MANAGER V1.3     ")
    print("*****************************************")
    print(ASCII_ART)

    choice = input("Press 1 to save a new password, 2 to search for a password, 3 to delete a password and 4 to view the list of services: ")

    #Save(1)
    if choice == "1":
        save_password(fernet)

    #View(2)    
    elif choice == "2":
        view_password(fernet)

    #Cancellation (3)
    elif choice == "3":
        if os.path.exists(PASSWORD_FILE):
            nome = input("Enter the name of the service containing the password to delete: ")
            with open(PASSWORD_FILE, "r") as file:
                lines = file.readlines()
            
            found = False
            with open(PASSWORD_FILE, "w") as file:
                for line in lines:
                    if not line.startswith(nome + ":"):
                        file.write(line)
                    else:
                        found = True
            
            if found:
                print("The password for " + nome + " has been deleted.")
            else:
                print("No password found with this name.")

    #List services (4)
    elif choice == "4":
        lista_servizi()

    #Invalid choice
    if (os.path.exists(PASSWORD_FILE)) and (choice != "1") and (choice != "2") and (choice != "3") and (choice != "4"):
        print("Invalid choice!")

#-----------------------------------------------------------

#Fernate object creation function
if __name__ == "__main__":
    if not os.path.exists(MASTER_FILE):
        fernet = crea_master_password()
    else:
        fernet = verificate_master_password()

    print("Access granted to the password manager!")
    main(fernet)
    input("\nPress Enter to exit...")

#----------------------------------------------------------------------------------------------------------------------------------------
#This program is free and open source, you can modify it and test it as many times as you want, but don't commercalize it or sell it without the author's permission.
#If you want to contact the author, you can find contact information on the repo's page on github.
#This program has a MIT license, as the github repo says.

#Last update: 07/09/2026 (Update the date if you modify it!)