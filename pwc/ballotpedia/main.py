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
from selenium.webdriver.support.ui import Select
from funcs import *



base_url = 'https://ballotpedia.org'
chrome_driver_path = 'C:\\data\\chromedriver\\chromedriver.exe'
serv_obj = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver =webdriver.Chrome(service=serv_obj, options=options)
driver.maximize_window()
url = 'https://ballotpedia.org/Elections_by_state_and_year'
driver.get(url)
time.sleep(1)

body_content = driver.find_element(By.XPATH,"//div[@class='mw-parser-output']")
if not body_content is None:
    print("body_content found")
    all_h2 = body_content.find_elements(By.TAG_NAME,'h2')
    # all_p = body_content.find_elements(By.XPATH,"//h2//following-sibling::p")
    # for p in all_p:
    #     print(p.find_element(By.XPATH,""))
    #     print(p.text)
    #     # break
    for h2 in all_h2:
        if h2.text.isnumeric():
            print(h2.text)
            try:
                elections_by_state = h2.find_element(By.XPATH,".//following-sibling::p")
            except:
                print("elections_by_state not found")    
                hidden_div = h2.find_element(By.XPATH,".//following-sibling::div[@class='scrollable-table-container auto-width']")
                hidden_div.find_element(By.XPATH,".//a[contains(.,'show')]").click()
                elections_by_state = hidden_div.find_element(By.XPATH,"./table[1]/tbody[1]/tr[2]/td[1]/p[1]")
                
            if not elections_by_state is None:
                all_state = elections_by_state.find_elements(By.TAG_NAME,'a')
                for state in all_state:
                    # state_election_url = base_url + state.get_attribute('href')
                    print(state.text,' = ', state.get_attribute('href'))
                    state_election(state.get_attribute('href'))
                    break
                # break
            break    
else:
    print("body_content not found")
