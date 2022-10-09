import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import csv



chrome_path = 'C:\\data\\chromedriver\\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
# driver = webdriver.Chrome(options=options, executable_path=chrome_path)
driver = webdriver.Chrome(options=options)

url = 'https://www.lofty.ai/marketplace'
driver.get(url)
time.sleep(5)
html_soup = BeautifulSoup(driver.page_source, 'html.parser')
properties = html_soup.select('div.property-card')
cont = 1
fails = 0
for properti in properties:
    detail_url = properti.select_one('a')['href']
    full_detail_url = 'https://www.lofty.ai' + detail_url
    driver2 = webdriver.Chrome(options=options, executable_path=chrome_path)
    driver2.get(full_detail_url)
    # time.sleep(6)
    delay = 15
    try:
        check = WebDriverWait(driver2,delay).until(EC.presence_of_element_located((By.TAG_NAME,'h1')))
        soup = BeautifulSoup(driver2.page_source, 'html.parser')    
        name = soup.select_one('h1')
        print(cont,full_detail_url)
        if name != None:
            print(cont,name.text)
        cont += 1
        driver2.close
    except TimeoutException:
        print('Failed to load! Timeout! ')
        fails += 1

print(fails)            
    
