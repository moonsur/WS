import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time



chrome_path = 'C:\\data\\chromedriver\\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path=chrome_path)

url = 'https://tel.search.ch/'
search_key = 'bern'
parameters = 'wo='+search_key+'&private=1'
full_url = url+parameters
# parameters = {
#     'wo':'bern',
#     'private':1,
# }
cont = 1
driver.get(full_url)
for _ in range(20):
    driver.execute_script("window.scrollTo(1, 50000)")
    time.sleep(1)
#r = requests.get(url, params=parameters)
# r = requests.get(full_url)
# html_soup = BeautifulSoup(r.text, 'html.parser')
html_soup = BeautifulSoup(driver.page_source, 'html.parser')
# pp = driver.find_elements(By.CLASS_NAME, 'tel-resultentry')
# for p in pp:

people = html_soup.select('table.tel-resultentry')
for person in people:
    name = person.select_one('h1')
    print(str(cont),name.text)
    cont += 1

