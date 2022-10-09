import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv



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
scroll_pause_time = 1.5 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:   
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)  
    scroll_height = driver.execute_script("return document.body.scrollHeight;") 
    if (screen_height) * i > scroll_height:
        break


html_soup = BeautifulSoup(driver.page_source, 'html.parser')

headers = ['Url','nom', 'adresse', 'code_postal',	'ville', 'tel',	'fax', 'latitude', 'longitude',	'tel_marketing_accept']
data = []
people = html_soup.select('table.tel-resultentry')
for person in people:    
    detail_Page_url = person.select_one('h1>a')    
    detail_url_full = url + detail_Page_url['href']
    # print(detail_url_full)
    r = requests.get(detail_url_full)
    soup = BeautifulSoup(r.text, 'html.parser')
    person_name = soup.select_one('h1').text
    address = soup.select_one('span.street-address').text
    post_code = soup.select_one('span.tel-zipcity>span.postal-code').text
    ville = soup.select_one('span.tel-zipcity>span.locality').text
    # tell = soup.select_one('table.sl-contact-table').select_one('span.sl-nowrap').text
    tell = soup.select_one('nav.tel-action-oneline').select_one('a.sl-icon-call')
    if tell != None:
        tell = tell.text
    else:
        tell = ''    
    fax = ''
    lat = ''
    lon = ''
    tel_m = ''
    single_data = [detail_url_full,person_name, address, post_code, ville, tell, fax, lat, lon, tel_m]
    data.append(single_data)
    # print(str(cont),single_data)
    cont += 1
print(cont)
with open('People-info.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(data)