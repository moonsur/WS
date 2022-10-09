from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_path = 'C:\\data\\chromedriver\\chromedriver.exe'
serv_obj = Service(chrome_path)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=serv_obj,options=options)

url = 'https://www.indeed.com/'
driver.get(url)
driver.maximize_window()
time.sleep(2)

driver.find_element(By.ID, 'text-input-what').send_keys('python developer')
driver.find_element(By.CLASS_NAME,'yosegi-InlineWhatWhere-primaryButton').click()
time.sleep(3)
# jobtitle = driver.find_element(By.XPATH,"//table[@class='jobCard_mainContent']//h2[@class='jobTitle']//a").text
# jobtitle = driver.find_element(By.PARTIAL_LINK_TEXT,"Python Developer")
jobtitle = driver.find_element(By.CSS_SELECTOR,"a.jcs-JobTitle")
print(jobtitle.get_attribute('href'))
print(jobtitle.text)
company_name = driver.find_element(By.CSS_SELECTOR,"div.companyInfo")
# print(company_name.find_element(By.CSS_SELECTOR,"a.companyOverviewLink[data-tn-element=companyName]").text)
print(company_name.find_element(By.XPATH,"//a[@class='companyOverviewLink'or @data-tn-element='companyName']").text) # @data-tn-element is not work

# "//*[contains(@id,'st')]"
# "//*[contains(@class,'st')]"
# "//*[starts-with(@id,'st')]"
# "//*[starts-with(@class,'st')]"
# "//a[text()='Find jobs']"
