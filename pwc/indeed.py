from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv

def number_contain(s):
    return any(char.isdigit() for char in s)

chrome_driver_path = 'C:\\data\\chromedriver\\chromedriver.exe'
serv_obj = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=serv_obj, options=options)
driver.maximize_window()
url ="https://www.indeed.com/"
driver.get(url)
time.sleep(1)
driver.find_element(By.CSS_SELECTOR,"input#text-input-what").send_keys('python developer')
driver.find_element(By.XPATH,"//button[@class='yosegi-InlineWhatWhere-primaryButton']").click()
time.sleep(1)
page = 1
cont = 1 
headers = ['Job Title', 'Company Name', 'Company Ratings', 'Location', 'Salary', 'Job Type']
data = []
delay = 10
while True:    
    jobs = driver.find_elements(By.XPATH,"//div[@class='job_seen_beacon']//td[@class='resultContent']")
    # print(jobs)
    print("job len= ",len(jobs))
      
    for job in jobs:
        # print(job.text)
        job_title = job.find_element(By.XPATH, ".//h2/a").text
        # job_title = ' - '.join(job_title.split())
        # job_title = job_title.replace('-')
        print(cont,job_title.strip())
        cont += 1
        company_name = job.find_element(By.XPATH,".//div[@class='heading6 company_location tapItem-gutter companyInfo']/span[@class='companyName']").text
        print(company_name.strip())
        try:
            company_rating = job.find_element(By.XPATH,".//div[@class='heading6 company_location tapItem-gutter companyInfo']/span[@class='ratingsDisplay withRatingLink']").text            
        except:
            company_rating = '' 
        print(company_rating.strip()) 

        company_location = job.find_element(By.XPATH,".//div[@class='heading6 company_location tapItem-gutter companyInfo']/div[@class='companyLocation']").text 
        try:
            other_location = job.find_element(By.XPATH,".//div[@class='heading6 company_location tapItem-gutter companyInfo']/div[@class='companyLocation']/span[@class='more_loc_container']").text 
        except:
            other_location = ''  
        if other_location != '':      
            company_location = company_location.replace(other_location, '')
        company_location = company_location.strip()    
        company_location = ', '.join([s.strip() for s in company_location.split('\n') if s.strip() !=''])
            
        print(company_location.strip())

        try:
            # salary = job.find_element(By.XPATH, ".//div[contains(@class,'metadata estimated-salary-container')]/span[@class='estimated-salary']/span").text
            salary = job.find_element(By.XPATH, ".//div[contains(@class,'salaryOnly')]/div[1]").text
            if number_contain(salary.strip()):
                job_type = ''
            else:
                job_type = salary
                salary = ''
                
        except:
            salary = ''
        print(salary.strip())  
        if job_type == '':
            try: 
                # job_type = job.find_element(By.XPATH,".//div[contains(@class,'attribute_snippet')]").text
                job_type = job.find_element(By.XPATH, ".//div[contains(@class,'salaryOnly')]/div[2]").text
            except:
                job_type = ''    
        print(job_type.strip())     
        print("-"*80)
        data.append([job_title.strip(), company_name.strip(), company_rating.strip(), company_location.strip(), salary.strip(), job_type.strip()])
    page += 1
    print('page no = ',page)
    if page > 10:
        break
    
    try:
        check = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,".//a[contains(@aria-label,'Next')]"))).click()        
    except TimeoutException:
        print("time out ... but not found Next button")  
        break  
    # driver.find_element(By.XPATH,".//a[contains(@aria-label,'Next')]").click()
    time.sleep(3)    

    # driver.find_element(By.XPATH, "//a[@data-testid='pagination-page-next' or @aria-label='Next Page']").click()
    # time.sleep(2)
    # below_nav = driver.find_element(By.XPATH, "//div[@id='mosaic-belowJobResultsPagination']")
    # print(below_nav.get_attribute('innerHTML'))
    # nav_f = driver.find_element(By.XPATH, "//div[@id='mosaic-belowJobResultsPagination']/preceding-sibling::nav")
    # print(nav_f.get_attribute('innerHTML'))
    # nav_divs = driver.find_elements(By.XPATH, "//nav[@aria-label='pagination']/child::*")
    # nav_divs = nav_f.find_elements(By.XPATH, "./child::*")
    # print(nav_divs)
    # print('nav len = ',len(nav_divs))
    # print(nav_divs[-1].get_attribute('innerHTML'))
    # nav_divs[-1].find_element(By.TAG_NAME,"a").click()
    # nav_divs[-1].find_element(By.XPATH,"./a").click()    
    # driver.find_element(By.CSS_SELECTOR, "a[data-testid=pagination-page-next]").click()

with open('jobs-info.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(data)
