import sqlite3
import os
from hashlib import sha256
from config_me import read_config

if os.path.exists('.env'):
    print('Welcome back, myself.')
    admin_pass = read_config('.env')
else:
    admin_pass = read_config('.config')

def checkin():
    auth = False
    while auth == False:    
        if input("What is your password?\n") != admin_pass:
            continue
        auth = True
    conn = sqlite3.connect('pwds.db')
    checkdb_exists(conn)

"""
def create_password(pass_key, service, admin_pass):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[:15]

def get_hex_key(admin_pass, service):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

def get_password(admin_pass, service):
    secret_key = get_hex_key(admin_pass, service)
    cursor = conn.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')

    file_string = ""
    for row in cursor:
        file_string = row[0]
    return create_password(file_string, service, admin_pass)

def add_password(service, admin_pass):
    secret_key = get_hex_key(admin_pass, service)

    command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' %('"' + secret_key +'"')        
    conn.execute(command)
    conn.commit()
    return create_password(secret_key, service, admin_pass)
"""

def checkdb_exists(conn):
    try:
        conn.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        print("Your safe has been created!\nWhat would you like to store in it today?")
    except:
        print("You have a safe, what would you like to do today?")
    showmenu()

"""
if connect == ADMIN_PASSWORD:
    try:
        conn.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        print("Your safe has been created!\nWhat would you like to store in it today?")
    except:
        print("You have a safe, what would you like to do today?")
""" 
    
def showmenu():
    user_option = input("q: Quit app\ng: Get login credentials for a site\ns: Save new login credentials for a site\np: Print username and password on site login\n")
    if user_option == 'q':
        return
    elif user_option == 'g':
        get_logins()
    elif user_option == 's':
        save_logins()
    elif user_option == 'p':
        print_logins()

def get_logins():
    pass

def save_logins():
    pass

def print_logins():
    pass

"""
    while True:
        print("\n"+ "*"*15)
        print("Commands:")
        print("q = quit program")
        print("gp = get password")
        print("sp = store password")
        print("*"*15)
        input_ = input(":")

        if input_ == "q":
            break
        if input_ == "sp":
            service = input("What is the name of the service?\n")
            print("\n" + service.capitalize() + " password created:\n" + add_password(service, ADMIN_PASSWORD))
        if input_ == "gp":
            service = input("What is the name of the service?\n")
            print("\n" + service.capitalize() + " password:\n"+get_password(ADMIN_PASSWORD, service))
"""
if __name__ == "__main__":
    checkin()