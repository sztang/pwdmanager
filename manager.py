import sqlite3
import os
from hashlib import sha256
from config_me import read_config

if os.path.exists('.env'):
    print('Welcome back, myself.')
    admin_pass = read_config('.env')
else:
    admin_pass = read_config('.config')

conn = ''
c = ''

def checkin():
    global conn, c
    auth = False
    while auth == False:    
        if input("What is your password?\n") != admin_pass:
            continue
        auth = True
    conn = sqlite3.connect('pwds.db')
    c = conn.cursor()
    checkdb_exists(c)

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

def checkdb_exists(c):
    try:
        c.execute('''CREATE TABLE credentials
            (website text PRIMARY KEY, username text, password text);''')
        print("New login credentials database created.")
    except:
        pass
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
    user_option = input("\n***************\nq: Quit app\ng: Get login credentials for a site\ns: Save new login credentials for a site\ne: Edit credentials for an existing account\np: Print username and password on site login\n")
    if user_option == 'q':
        conn.commit()
        conn.close()
        return
    elif user_option == 'g':
        get_logins()
    elif user_option == 's':
        save_logins()
    elif user_option == 'p':
        print_logins()
    elif user_option == 'e':
        edit_rows()
    elif user_option == 'ALL': # Hidden option
        get_all()
    else:
        print('Invalid input. Enter one of the following:')
    showmenu()

def get_logins(website=None):
    global c
    if not website:
        website = (input('Get credentials for which website?\n'))
    rows = c.execute("SELECT rowid, * from credentials WHERE website=?", (website,)).fetchall()
    if len(rows) > 1:
        print("There are multiple entries for {}. Let's clean up our act.".format(website))
        for r in rows:
            print(r)
        clear = int(input("Enter index of row you'd like to delete."))
        clear_rows(rows[clear])
        return 'ERROR'
    else:
        username = rows[0][2]
        password = rows[0][3]
        # print(rows[0])
        print('Username: {} | Password: {}'.format(username, password))
        return 'OK'

def get_all():
    global c
    print(c.execute("SELECT * FROM credentials").fetchall())

def save_logins():
    global conn, c
    website = str(input('Website:\n'))
    username = str(input('Username:\n'))
    password = str(input('Password:\n'))
    c.execute("INSERT INTO credentials (website,username,password) VALUES (?,?,?)",(website,username,password))
    if get_logins(website=website) == 'OK':
        print("Credentials added, you're good to go.")
    return

def print_logins(): # WIP
    pass

def clear_rows(row=None): # WIP
    if row:
        print(c.execute("SELECT * from credentials WHERE id=?", row[0]))
        if input("Are you sure you want to delete this? [y/n]") in ['y','Y']:
            c.execute("DELETE FROM credentials WHERE id=?",row[0])
    if not row:
        print("Did you just ask to delete the whole table?")

def edit_rows(website=None): # WIP
    if not website:
        website = (input('Edit credentials for which website?\n'))
    row = c.execute("SELECT rowid, * from credentials WHERE website=?", (website,)).fetchone()
    new_username = str(input('Enter new username: \n'))
    new_password = str(input('Enter new username: \n'))
    c.execute("UPDATE credentials SET username=?, password=? WHERE rowid=?",(new_username, new_password, row[0],))
    if get_logins(website) == 'OK':
        print("Credentials updated - you're good to go.")
    else:
        print("There's been some error.")

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