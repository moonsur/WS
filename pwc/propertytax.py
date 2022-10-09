from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import csv

def number_contain(s):
    return any(char.isdigit() for char in s)

chrome_driver_path = 'C:\\data\\chromedriver\\chromedriver.exe'
serv_obj = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=serv_obj, options=options)
driver.maximize_window()
url = "https://propertytax.vi.gov/"
driver.get(url)
time.sleep(2)
driver.find_element(By.XPATH, "//input[@value='PROPERTY SEARCH']").click()
driver.switch_to.frame(driver.find_element(By.TAG_NAME,"iframe"))
driver.find_element(By.XPATH, "//input[@id='NameSearchText']").send_keys('krigger-johnson')
driver.find_element(By.XPATH, "//input[@id='Search']").click()
driver.find_element(By.XPATH, "//table[@id='GridView1']//tr[@id='GridView1_RowId_0']")
#driver.switch_to.default_content() # to switch to default
time.sleep(2)