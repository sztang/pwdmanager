# Password Manager

### Saves usernames and passwords for websites into a simple SQLite database with a python interface.

**When using for the first time**, run config_me.py to set your admin password to the manager app. Terminal code:
```cd ~/path/to/directory```
```python config_me.py```

**Paste the code from bash_custom.sh** into your .bash_profile and replace filepath to use the pwd terminal shortcut; once set up, just type ```pwd``` in the terminal to run the ```pwdmanager```.

**If not using the bash shortcut**, run manager.py to access the ```pwdmanager```. Terminal code:
```cd ~/path/to/directory```
```python manager.py```

### pwdmanager Functions
1. **Get** login credentials
2. **Save** login credentials
3. **Edit** login credentials
4. (Open a website login page and) **Print** login credentials