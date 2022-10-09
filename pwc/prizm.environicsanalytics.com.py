from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup


url = 'https://prizm.environicsanalytics.com/'
chrome_path = 'C:\\data\\chromedriver\\chromedriver.exe'
# serv_obj = Service(chrome_path)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(service=serv_obj, options=options)
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(url)
time.sleep(2)
# print(driver.page_source)
title = driver.find_element(By.TAG_NAME,'h1')
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# title = soup.find('h1')
print(title.text)
driver.find_element(By.XPATH,"//form[@class='postal-lookup__input']//input").send_keys('N6A3X5')
# driver.find_element(By.TAG_NAME,'input').send_keys('N6A3X5')
# print(search_input.text)
driver.find_element(By.XPATH,"//form[@class='postal-lookup__input']//button").click()
time.sleep(5)
print(driver)
soup = BeautifulSoup(driver.page_source, 'html.parser' )
section = soup.select_one('ul.segment-details__section')
title = section.select_one('h2.title--secondary')
print(title.text)

