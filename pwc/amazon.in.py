from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import csv

def number_contain(s):
    return any(char.isdigit() for char in s)

# chrome_driver_path = 'C:\\data\\chromedriver\\chromedriver.exe'
edge_driver_path = 'C:\\data\\\edgedriver\\msedgedriver.exe'
# serv_obj = Service(chrome_driver_path)
serv_obj = Service(edge_driver_path)
# options = webdriver.ChromeOptions()
options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(service=serv_obj, options=options)
driver = webdriver.Edge(service=serv_obj, options=options)
driver.maximize_window()
# url ="https://www.amazon.in/s?i=kitchen&bbn=5925789031&rh=n%3A5925789031%2Cp_72%3A1318476031&s=review-rank&dc&fs=true&qid=1664906800&rnid=1318475031&ref=sr_st_review-rank&ds=v1%3AZuVRtHPZNCw2knT1XbkM7PwthXuzR%2BwnsBeOVAkeDKE"
url = "https://www.amazon.in/"
driver.get(url)
time.sleep(1)

# products = driver.find_elements(By.XPATH, "//div[@class='a-section a-spacing-base']")
# print(len(products))

driver.find_element(By.XPATH, "//div[@id='nav-main']/div[@class='nav-left']").click()
# time.sleep(1)
driver.find_element(By.XPATH, "//div[@id='hmenu-content']//a[@class='hmenu-item hmenu-compressed-btn']").click()
# time.sleep(1)
driver.find_element(By.XPATH, "//a[contains(.,'Home, Kitchen, Pets')]").click()
# time.sleep(1)
driver.find_element(By.XPATH, "//a[contains(.,'Kitchen & Dining')]").click()
time.sleep(4)
driver.find_element(By.XPATH, "//a[contains(.,'See all results')]").click()
time.sleep(3)
x = driver.find_element(By.XPATH, "//select[@id='s-result-sort-select']")
drop=Select(x) 
drop.select_by_visible_text("Avg. Customer Review")
time.sleep(3)
titles = driver.find_elements(By.XPATH,"//h2[contains(@class,'a-size-mini a-spacing-none a-color-base s-line-clamp-')]")
# a-size-mini a-spacing-none a-color-base s-line-clamp-3
# a-size-mini a-spacing-none a-color-base s-line-clamp-4
cont = 1
for title in titles:
    print(cont,title.text)
    cont += 1