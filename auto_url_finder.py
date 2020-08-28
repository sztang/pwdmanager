from googleapiclient.discovery import build
import webbrowser
import os
from selenium import webdriver
from config_me import read_config
from googlesearch import search

def find_url(query):
    if os.path.exists('.env'): # For personal use, private Google API keys
        API_KEY = read_config('.env',readAPI=True)['API_KEY']
        CSE_ID = read_config('.env',readAPI=True)['CSE_ID']
        service = build("customsearch", "v1", developerKey=API_KEY)
        query_results = service.cse().list(q=query,cx=CSE_ID).execute()
        link_list = []
        for result in query_results['items']:
            link_list.append(result['link'])
        print('Found URL: ',link_list[0])
        return link_list[0]
    else: # For general use without API keys
        for u in search(query, stop = 1):
            return u

def open_and_input(url, query_username, query_password):
    driver = webdriver.Chrome()
    driver.get(url)
    username = driver.find_element_by_id('username')
    password = driver.find_element_by_id('password')
    username.send_keys(query_username)
    password.send_keys(query_password)
    
    quitdriver = input("Enter 'q' to quit Selenium driver.\n")
    while quitdriver not in ['q','Q']:
        continue
    driver.close()

if __name__ == "__main__":
    webbrowser.open(find_url('Github'))