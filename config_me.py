import configparser

def read_config(config_name, readAPI=False):
    config = configparser.ConfigParser()
    config.read(config_name)
    if not readAPI:
        return config['DEFAULT']['user_pass']
    else:
        return {'API_KEY':config['API']['API_KEY'],'CSE_ID':config['API']['CSE_ID']}

def set_admin_pass(config_pass):
    if config_pass == '':
        password_set = False
        while password_set == False:
            admin_pass = input("Set your admin password.\n")
            if admin_pass == "":
                print('A password needs to be SOMETHING...')
                continue
            password_set = True
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'user_pass': admin_pass}
        with open('.config', 'w') as configfile:
            config.write(configfile)
        print("You're good to go.")
        return
    else:
        option = input('Your admin password has already been set. [ANY KEY: quit / r: reset password]\n')
        if option == 'r':
            reset_admin_pass()
        else:
            return

def reset_admin_pass():
    password_set = False
    while password_set == False:
        new_pass = input("Enter your new password.\n")
        if new_pass == "":
            print('A password needs to be SOMETHING...')
            continue
        password_set = True
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'user_pass': new_pass}
    with open('.config', 'w') as configfile:
        config.write(configfile)
    print("You're good to go.")

if __name__ == "__main__":
    # Execute this the very first time using the app to set new admin password
    set_admin_pass(read_config('.config'))