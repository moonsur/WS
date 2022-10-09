import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
#options.add_argument('--headless')

driver = webdriver.Chrome('C:\\data\\chromedriver\\chromedriver.exe', chrome_options=options)

url = 'https://www.francetravauxsurcordes.fr/adherents/page/2/'
driver.get(url)
time.sleep(2)
source = driver.page_source
headers = ['Name (title)','Sector (subtitle)','Adress','Email','Description']
data = []
#r = requests.get(url)
#html_soup = BeautifulSoup(r.text, 'html.parser')
html_soup = BeautifulSoup(source, 'html.parser')
companies = html_soup.select('div.list-preview-body')
for company in companies:
    row = []
    name = company.select_one('h2.list-preview-title').text
    #print(name)
    row.append(name)
    sectors = []
    for s in company.select('li.list-preview-field'):
        sectors.append(s.text)
    sector = ' - '.join(sectors)
    #print(sector)
    row.append(sector)
    address = company.select_one('li.list-preview-address').text
    #print(address.split(','))
    row.append(address)
    email = company.select_one('li.list-preview-email').text
    #print('Email:',email) 
    row.append(email)
    description = company.select_one('p').text
    #print(description)
    row.append(description)  
    data.append(row)


with open('companyinfo.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(headers)

    # write multiple rows
    writer.writerows(data)    
