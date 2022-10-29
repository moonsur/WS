import time
import requests
# from createtables import create_tables
# from insertUpdate import *
import psycopg2
# from config import config
from datetime import datetime, timezone
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


chrome_driver_path = 'C:\\data\\chromedriver\\chromedriver.exe'
serv_obj = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])


def state_election(state_url):
    driver_by_state =webdriver.Chrome(service=serv_obj, options=options)
    driver_by_state.maximize_window()    
    driver_by_state.get(state_url)
    time.sleep(1)
    all_elections = driver_by_state.find_elements(By.XPATH, "//table[@class='marqueetable']//a[not(contains(.,'Click here'))]")
    for election in all_elections:
        print(election.text)
    driver_by_state.close()