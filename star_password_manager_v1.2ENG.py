# Questo è il codice di Star Password Manager, se stai leggendo questo, in questo codice torverai commenti facili da leggere, caoire e testare il codice a tuo piacimento. Buon lavoro!
# ATTENZIONE: Questo programma è open source. E' possibile modificarlo e testarlo a proprio piacimennto, ma non è possibile commercializzarlo o rivenderlo senza il consenso dell'autore.
#Per qualsiasi informazione, è possibile contattare l' autore tramite la mail messa appsoitamnete sulla pagina del progetto su Github.

#STAR PASSWORD MANAGER V1.2
#-----------------------------------------------------------

#Import list
import os
import base64
import hashlib
from getpass import getpass
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

def _deriva_hash(password, salt):
    return hashlib.pbkdf2_hmac(HASH_ALGO, password.encode("utf-8"), salt, ITERATIONS)
 
 #Password CREATION

def crea_master_password():
    print("Welcome! You need to create a master password at the first launch of the program to protect your passwords (Don't forget it!).")
    while True:
        #CREATION AND CONFERMATION
        pwd1 = getpass("Create a master password: ")
        pwd2 = getpass("Confirm the master password: ")
        #EQUALITY check
        if pwd1 == pwd2:
            break
        print("The passwords do not match. Please try again.\n")
 
    salt = secrets.token_bytes(SALT_BYTES)
    pwd_hash = _deriva_hash(pwd1, salt)
 
    dati = {"salt": salt.hex(), "hash": pwd_hash.hex()}
    with open(MASTER_FILE, "w") as f:
        json.dump(dati, f)
 
    print("Master password created and saved successfully. Have Fun using the program!\n")
 
 #Password VERIFICATION

def verificate_master_password():
    with open(MASTER_FILE, "r") as f:
        dati = json.load(f)
 
    salt = bytes.fromhex(dati["salt"])
    hash_salvato = bytes.fromhex(dati["hash"])
    
 #master password INPUT and VERIFICATION
    while True:
        pwd = getpass("Enter the master password: ")
        hash_calcolato = _deriva_hash(pwd, salt)
 
        if hmac.compare_digest(hash_calcolato, hash_salvato):
            print("Access granted.\n")
            break
        print("Password incorrect, try again.\n")

#Recall the function for the creation and verification of the Master Password.         
if __name__ == "__main__":
    if not os.path.exists(MASTER_FILE):
        crea_master_password()
    else:
        verificate_master_password()
 
    print("Access granted to the password manager!")
#-----------------------------------------------------------
#BASE64 ENCRYPTION AND DECRYPTION

#Base64 encryption and decryption, the passwords will be saved on a .txt file with the name of the service and the encrypted password, it will decrypt the password when you search for it in the program.
def cifra(testo):
    return base64.b64encode(testo.encode()).decode()

def decifra(testo):
    return base64.b64decode(testo.encode()).decode()
#-----------------------------------------------------------
#FUNCTIONS TO SAVE,DELETE AND VIEW PASSWORDS (the delete password function is in the next part of the code, i guess if it works i'll leave it here -if it works,don't touch it- :D)

# Save password function
def save_password():
    nome = input("Enter the name of the application: ")
    password = input("Enter the password: ")
    password_cifrata = cifra(password)
    with open("password.txt", "a") as file:
        file.write(nome + ":" + password_cifrata + "\n")
    print("The password has been saved!")

# View password function

def view_password():
    nome = input("Enter the name of the application to search for: ")
    if os.path.exists("password.txt"):
        trovato = False
        with open("password.txt", "r") as file:
            for line in file:
                if line.startswith(nome + ":"):
                    parti = line.split(":", 1)
                    print("The password is: " + decifra(parti[1].strip()))
                    trovato = True
                    break
        if not trovato:
            print("No password found for this name.")
    else:
        print("There are no passwords saved yet.")

# List services function

def lista_servizi():
     if os.path.exists("password.txt"):
        with open("password.txt", "r") as file:
            servizi = [line.split(":", 1)[0] for line in file if line.strip()]
        if servizi:
            print("Servizi salvati:")
            for servizio in servizi:
                print("- " + servizio)

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

def main():
    print("*****************************************")
    print("       STAR PASSWORD MANAGER V1.2      ")
    print("*****************************************")
    print(ASCII_ART)

    choice = input("Press 1 to save a new password, 2 to search for a password, 3 to delete a password and 4 to view the list of services: ")

    #Save(1)
    if choice == "1":
        save_password()

    #View(2)    
    elif choice == "2":
        view_password()

    #Cancellation (3)
    elif choice == "3":
        if os.path.exists("password.txt"):
            nome = input("Enter the name of the service containing the password to delete: ")
            with open("password.txt", "r") as file:
                lines = file.readlines()
            
            found = False
            with open("password.txt", "w") as file:
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
    if ("password.txt") and (choice != "1") and (choice != "2") and (choice != "3") and (choice != "4"):
        print("Invalid choice!")

if __name__ == "__main__":
            main()
            input("\nPress Enter to exit...")
#----------------------------------------------------------------------------------------------------------------------------------------
#This program is free and open source, you can modify it and test it as many times as you want, but don't commercalize it or sell it without the author's permission.
#If you want to contact the author, you can find contact information on the repo's page on github.
#This program has a MIT license, as the github repo says.

#Last update: 28/08/2026 (Update the date if you modify it!)