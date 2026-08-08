# Questo è il codice di Star Password Manager, se stai leggendo questo, in questo codice torverai commenti facili da leggere, caoire e testare il codice a tuo piacimento. Buon lavoro!
# ATTENZIONE: Questo programma è open source. E' possibile modificarlo e testarlo a proprio piacimennto, ma non è possibile commercializzarlo o rivenderlo senza il consenso dell'autore.
#Per qualsiasi informazione, è possibile contattare l' autore tramite la mail messa appsoitamnete sulla pagina del progetto su Github.

#STAR PASSWORD MANAGER V1.2

#import necessari
import os
import base64
import hashlib
from getpass import getpass
import secrets
import json
import hmac

#Variabili master password
MASTER_FILE = "master.json"
ITERATIONS = 200_000
HASH_ALGO = "sha256"
SALT_BYTES = 16

#Master Password (Inserimento password primo avvio)

def _deriva_hash(password, salt):
    return hashlib.pbkdf2_hmac(HASH_ALGO, password.encode("utf-8"), salt, ITERATIONS)
 
 #Creazione password

def crea_master_password():
    print("Benvenuto! è necessario creare una master password al primo avvio del programma per proteggere le password ad ogni accesso.")
    while True:
        #creazione e conferma password
        pwd1 = getpass("Crea una master password: ")
        pwd2 = getpass("Conferma la master password: ")
        #Controllo coincidenza password
        if pwd1 == pwd2:
            break
        print("Le due password non coincidono. Riprova.\n")
 
    salt = secrets.token_bytes(SALT_BYTES)
    pwd_hash = _deriva_hash(pwd1, salt)
 
    dati = {"salt": salt.hex(), "hash": pwd_hash.hex()}
    with open(MASTER_FILE, "w") as f:
        json.dump(dati, f)
 
    print("Master password creata e salvata correttamente.Buon utilizzo!\n")
 
 #Verifica password

def verifica_master_password():
    with open(MASTER_FILE, "r") as f:
        dati = json.load(f)
 
    salt = bytes.fromhex(dati["salt"])
    hash_salvato = bytes.fromhex(dati["hash"])
 #Inserimento Password salvata
    while True:
        pwd = getpass("Inserisci la master password: ")
        hash_calcolato = _deriva_hash(pwd, salt)
 
        if hmac.compare_digest(hash_calcolato, hash_salvato):
            print("Accesso consentito.\n")
            break
        print("Password errata, riprova.\n")

#Richiamo delle funzioni sopra elencate         
if __name__ == "__main__":
    if not os.path.exists(MASTER_FILE):
        crea_master_password()
    else:
        verifica_master_password()
 
    print("Accesso al password manager riuscito!")


#Cifratura e decifratura base64
def cifra(testo):
    return base64.b64encode(testo.encode()).decode()

def decifra(testo):
    return base64.b64decode(testo.encode()).decode()

# Funzioni definite per salvare, visualuizzare e cancellare le password.

# Salva Password
def salva_password():
    nome = input("Inserisci il nome dell'applicazione: ")
    password = input("Inserisci la password: ")
    password_cifrata = cifra(password)
    with open("password.txt", "a") as file:
        file.write(nome + ":" + password_cifrata + "\n")
    print("La password è stata salvata!")

# Visualizza password

def visualizza_password():
    nome = input("Inserisci il nome dell'applicazione da cercare: ")
    if os.path.exists("password.txt"):
        trovato = False
        with open("password.txt", "r") as file:
            for line in file:
                if line.startswith(nome + ":"):
                    parti = line.split(":", 1)
                    print("La password è: " + decifra(parti[1].strip()))
                    trovato = True
                    break
        if not trovato:
            print("Nessuna password trovata per questo nome.")
    else:
        print("Non ci sono ancora password salvate.")

# Lista servizi

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
#Input ed output del programma con tutte le sue funzioni.

def main():
    print("*****************************************")
    print("       STAR PASSWORD MANAGER V1.2      ")
    print("*****************************************")
    print(ASCII_ART)

    scelta = input("Premi 1 per salvare una nuova password, 2 per cercare una password, 3 per cancellare una password e 4 per visualizzare la lista dei servizi: ")

    #Salvataggio (1)
    if scelta == "1":
        salva_password()

    #Visualizzazione (2)    
    elif scelta == "2":
        visualizza_password()

    #Cancellazione (3)
    elif scelta == "3":
        if os.path.exists("password.txt"):
            nome = input("Inserisci il nome del servizio contenente la password da cancellare: ")
            with open("password.txt", "r") as file:
                lines = file.readlines()
            
            trovato = False
            with open("password.txt", "w") as file:
                for line in lines:
                    if not line.startswith(nome + ":"):
                        file.write(line)
                    else:
                        trovato = True
            
            if trovato:
                print("La password di " + nome + " è stata cancellata.")
            else:
                print("Nessuna password trovata con questo nome.")

    #Lista servizi (4)
    elif scelta == "4":
        lista_servizi()

    if ("password.txt") and (scelta != "1") and (scelta != "2") and (scelta != "3") and (scelta != "4"):
        print("Scelta non valida!")

if __name__ == "__main__":
            main()
            input("\nPremi Invio per uscire...")
