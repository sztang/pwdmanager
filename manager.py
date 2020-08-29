import sqlite3
import os
from config_me import read_config
from auto_url_finder import find_url, open_and_input
import webbrowser
from selenium import webdriver
import pyperclip

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
        if input("What is your admin password?\n") != admin_pass:
            continue
        auth = True
    conn = sqlite3.connect('pwds.db')
    c = conn.cursor()
    checkdb_exists(c)

def checkdb_exists(c):
    try:
        c.execute('''CREATE TABLE credentials
            (website text PRIMARY KEY, url text, username text, password text);''')
        print("New login credentials database created.")
    except:
        pass
    showmenu()
    
def showmenu():
    user_option = input("\n***************\nq: Quit app\ng: Get login credentials for a site\ns: Save new login credentials for a site\ne: Edit credentials for an existing account\np: Print username and password on site login\nADMIN: Enter admin menu\n")
    if user_option == 'q':
        conn.commit()
        conn.close()
        return
    elif user_option == 'g':
        get_logins()
    elif user_option == 's':
        save_logins()
        conn.commit()
    elif user_option == 'p':
        website = input('Launch which website?')
        print_logins(website)
    elif user_option == 'e':
        edit_rows()
        conn.commit()
    elif user_option in ['ADMIN','admin']:
        showadminmenu()
    else:
        print('Invalid input. Enter one of the following:')
    showmenu()

def get_logins(website=None):
    global c
    if not website:
        website = (input('Get credentials for which website?\n'))
    rows = c.execute("SELECT rowid from credentials WHERE website=?", (website,)).fetchall()
    if len(rows) > 1:
        print("There are multiple entries for {}. Let's clean up our act.".format(website))
        for r in rows:
            print(r)
        clearid = str(input("Enter index of row you'd like to delete."))
        clear_rows(clearid)
        return 'ERROR'
    else:
        print('Row ID:',rows[0][0])
        username = c.execute("SELECT username from credentials WHERE rowid=?", (str(rows[0][0]),)).fetchone()[0]
        password = c.execute("SELECT password from credentials WHERE rowid=?", (str(rows[0][0]),)).fetchone()[0]
        print('Username: {} | Password: {}'.format(username, password))
        pyperclip.copy(password)
        return 'OK'

def get_all():
    global c
    list_of_tuples = c.execute("SELECT rowid, * FROM credentials").fetchall()
    for t in list_of_tuples:
        print(t)

def save_logins():
    global conn, c
    website = str(input('Website:\n'))
    url = str(input('URL:\n'))
    if url == '':
        url = find_url(website + ' login')
    username = str(input('Username:\n'))
    password = str(input('Password:\n'))
    c.execute("INSERT INTO credentials (website,url,username,password) VALUES (?,?,?,?)",(website,url,username,password,))
    if get_logins(website=website) == 'OK':
        print("Credentials added, you're good to go.")
    return

def print_logins(website):
    query = c.execute("SELECT rowid, url from credentials WHERE website=?", (website,)).fetchone()
    queryid = query[0]
    query_username = c.execute("SELECT username from credentials WHERE rowid=?", (queryid,)).fetchone()[0]
    query_password = c.execute("SELECT password from credentials WHERE rowid=?", (queryid,)).fetchone()[0]
    queryurl = query[1]
    open_and_input(queryurl,query_username,query_password)

def clear_rows(rowid=None):
    if rowid:
        print(c.execute("SELECT * from credentials WHERE rowid=?", (str(rowid),)).fetchone())
        if input("Are you sure you want to delete this? [y/n]") in ['y','Y']:
            c.execute("DELETE FROM credentials WHERE rowid=?",(str(rowid),))
            print('Entry deleted.')
        else:
            print('Deletion cancelled.')
    if not rowid:
        if input("Did you just ask to delete the whole table? [y/n] ") in ['y','Y']:
            if input("Enter your admin password again to confirm deletion.\n") == admin_pass:
                c.execute("DROP TABLE credentials")
                print('Credentials table deleted.')
            else:
                print('Database KILL not executed.')

def edit_rows(website=None):
    if not website:
        website = (input('Edit credentials for which website?\n'))
    row = c.execute("SELECT rowid, * from credentials WHERE website=?", (website,)).fetchone()
    new_username = str(input('Enter new username (Hit ENTER to use existing): \n'))
    new_password = str(input('Enter new password (Hit ENTER to use existing): \n'))
    new_url = str(input("Enter new URL (Hit ENTER to use existing): \n"))
    if '' not in [new_username,new_password,new_url]:
        c.execute("UPDATE credentials SET username=?, password=? WHERE rowid=?",(new_username, new_password, row[0],)) # changing all: include URL
    elif new_url == '':
        if '' not in [new_username,new_password]: # URL empty, but both user and pass updated
            c.execute("UPDATE credentials SET username=?, password=? WHERE rowid=?",(new_username, new_password, row[0],)) #changing user and pass
        elif new_username == '': # URL empty, user empty
            if new_password == '': # nothing changed
                pass
            else: # Only password updated
                c.execute("UPDATE credentials SET password=? WHERE rowid=?",(new_password, row[0],)) # changing only pass
        else: # URL empty, pass empty
            c.execute("UPDATE credentials SET username=? WHERE rowid=?",(new_username, row[0],)) # changing only user
    elif new_username == '' and new_password == '':
        c.execute("UPDATE credentials SET username=? WHERE rowid=?",(new_username, row[0],)) # changing only URL - include URL
    elif new_username == '':
        c.execute("UPDATE credentials SET password=? WHERE rowid=?",(new_password, row[0],)) # changing URL and pass - include URL
    else:
        c.execute("UPDATE credentials SET username=? WHERE rowid=?",(new_username, row[0],)) # changing URL and user - include URL
    
    if get_logins(website) == 'OK':
        print("Credentials updated - you're good to go.")
    else:
        print("There's been some error.")

def showadminmenu(): # higher level admin controls
    user_option = input("\n***ADMIN_MENU***\nALL: Get all table entries\nDELETE: Delete specific row\nKILL: Delete entire table\nBACK: Return to standard menu\n")
    if user_option in ['ALL','all']:
        get_all()
    elif user_option in ['DELETE','delete']:
        get_all()
        clear_rows(str(input('Enter rowid of row to delete: ')))
    elif user_option in ['KILL','kill']:
        clear_rows()
    elif user_option in ['BACK','back']:
        showmenu()
    else:
        return

if __name__ == "__main__":
    checkin()