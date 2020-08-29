# Password Manager

#### Saves usernames and passwords for websites into a simple SQLite database with a python interface.

### Quickstart

**When using for the first time**, run config_me.py to set your admin password to the manager app. Terminal code:

```cd ~/path/to/directory```

```python config_me.py```

**Paste the code from bash_custom.sh** into your .bash_profile and replace filepath to use the pwd terminal shortcut; once set up, just type ```pwd``` in the terminal to run the ```pwdmanager```.

**If not using the bash shortcut**, run manager.py to access the ```pwdmanager```. Terminal code:

```cd ~/path/to/directory```

```python manager.py```

### pwdmanager Functions
1. **Get** login credentials (and copy password to clipboard)
2. **Save** login credentials
3. **Edit** login credentials
4. (Open a webpage and) **Print** login credentials

Login functions performed with Selenium ChromeDriver.

When saving an entry, if no login URL is specified, a Google search is performed on the website name and the first result is taken to be the URL.

When ```Print``` is called, Selenium opens the URL on file in the database and looks for elements on the page with ```id=username``` and ```id=password``` to enter your saved credentials. It will not automatically submit the page.

### pwdmanager Admin Functions
1. **ALL**: Get all credentials entries
2. **DELETE**: Delete specific entry
3. **KILL**: Wipe entire database