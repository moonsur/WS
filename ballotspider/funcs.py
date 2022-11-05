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
# from selenium.webdriver.edge.service import Service
import scrapy
from ballotspider.spiders import spider_classes as spc
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings




chrome_driver_path = 'C:\\data\\chromedriver\\chromedriver.exe'
serv_obj = Service(chrome_driver_path)
options = webdriver.ChromeOptions()

# edge_driver_path = 'C:\\data\\\edgedriver\\msedgedriver.exe'
# serv_obj = Service(edge_driver_path)
# options = webdriver.EdgeOptions()
# options.add_argument("headless")
# options.add_argument("disable-application-cache")
# options.add_argument("disk-cache-size=0")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# driver_by_state = webdriver.Chrome(service=serv_obj, options=options)
# driver_by_state.maximize_window() 

driver_election_info = webdriver.Chrome(service=serv_obj, options=options)
# driver_election_info = webdriver.Edge(service=serv_obj, options=options)
driver_election_info.maximize_window() 

driver_candidate_info = webdriver.Chrome(service=serv_obj, options=options)
# driver_candidate_info = webdriver.Edge(service=serv_obj, options=options)
driver_candidate_info.maximize_window() 

def state_election(state_name, election_year, state_url):
    driver_by_state = webdriver.Chrome(service=serv_obj, options=options)
    # driver_by_state = webdriver.Edge(service=serv_obj, options=options)
    driver_by_state.maximize_window()    
    driver_by_state.get(state_url)
    # time.sleep(1)
    all_us_senate_elections = []
    all_us_house_elections = []
    all_elections = driver_by_state.find_elements(By.XPATH, "//table[@class='marqueetable']//a[not(contains(.,'Click here'))]")
    for election in all_elections:
        if election.text.strip().lower() == "u.s. senate": 
            # print(election.text.strip().lower(), election.get_attribute('href'))            
            all_us_senate_elections.append((state_name, election_year, election.get_attribute('href')))
        elif election.text.strip().lower() == "u.s. house":
            # print(election.text.strip().lower(), election.get_attribute('href'))            
            all_us_house_elections.append((state_name, election_year, election.get_attribute('href'))) 

    driver_by_state.close()

    # for senate_election in all_us_senate_elections:
        # print(senate_election)
    #     us_senate(senate_election[0], senate_election[1], senate_election[2])

    for house_election in all_us_house_elections:
        print(house_election)
        us_house(house_election[0], house_election[1], house_election[2])

def us_senate(state_name, election_year, election_url):    
    driver_election_info.get(election_url)     
    voteboxes = driver_election_info.find_elements(By.XPATH, "//div[@class='votebox']") 
    for votebox in voteboxes:
        try:
            result_text = votebox.find_element(By.XPATH, ".//p[@class='results_text']").text.strip()            
            election_date = str.split(result_text,'on')[-1].replace('.','').strip()
            election_date_object = datetime.strptime(election_date, "%B %d, %Y")
            # election_date_arr = str.split(election_date, ' ')
            curr_el_year = str.split(election_date, ' ')[-1].strip()            
            if curr_el_year == election_year:
                election_name = votebox.find_element(By.XPATH,".//h5[@class='votebox-header-election-type']").text.strip()                
                print("Election Date:",election_date_object) 
                print('Election Name = ',election_name)
                result_table = votebox.find_element(By.XPATH, ".//table[@class='results_table']")
                result_rows = result_table.find_elements(By.XPATH, ".//tr[contains(@class,'results_row')]")
                for result_row in result_rows:                    
                    candidate_url = result_row.find_element(By.XPATH, ".//td[@class='votebox-results-cell--text']//a").get_attribute('href').strip()
                    print('Candidate URL = ', candidate_url)
                    candidate_info(candidate_url,election_name,election_date_object)
                    try:
                        votes_percentage = result_row.find_element(By.XPATH, ".//td[@class='votebox-results-cell--number'][1]").text.strip()
                    except:
                        votes_percentage = '' 
                    print('Votes Percentage = ', votes_percentage)       
                    try:
                        votes_number = result_row.find_element(By.XPATH, ".//td[@class='votebox-results-cell--number'][2]").text.strip()
                    except:
                        votes_number = '' 
                    print('Votes Number = ', votes_number)       

            # break
        except:
            continue 


def us_house(state_name, election_year, election_url):    
    driver_election_info.get(election_url)       
    voteboxes = driver_election_info.find_elements(By.XPATH, "//div[@class='votebox']")    
    if len(voteboxes) > 0:      
        # scrape_voteboxes(state_name, election_year, voteboxes)
        pass 
    else:
        district_election_urls = driver_election_info.find_elements(By.XPATH, "//h3[contains(.,'District') and ./span[contains(@id,'District')]]/following-sibling::dl[1]//a")
        lst_district_election_urls = [dis_ele_url.get_attribute('href').strip() for dis_ele_url in district_election_urls]
        print('Number of District = ',len(lst_district_election_urls))
        cont = 1
        for district_election_url in lst_district_election_urls:
            driver_election_info.get(district_election_url)
            xp = f"//div[@class='votebox' and .//p[contains(.,'{election_year}')]]"
            print(xp)
            voteboxes = driver_election_info.find_elements(By.XPATH, xp)    
            if len(voteboxes) > 0:      
                print('voteboxes lenght for district election = ',len(voteboxes))
                scrape_voteboxes(state_name, election_year, voteboxes)
            if cont > 1:
                break
            cont +=1
        
                   
           
        
def scrape_voteboxes(state_name, election_year, voteboxes):
    print('Into the scrape voteboxes')
    for votebox in voteboxes:
        try:
            result_text = votebox.find_element(By.XPATH, ".//p[@class='results_text']").text.strip()            
            election_date = str.split(result_text,'on')[-1].replace('.','').strip()
            election_date_object = datetime.strptime(election_date, "%B %d, %Y")
            # election_date_arr = str.split(election_date, ' ')
            curr_el_year = str.split(election_date, ' ')[-1].strip()            
            if curr_el_year == election_year:
                election_name = votebox.find_element(By.XPATH,".//h5[@class='votebox-header-election-type']").text.strip()                
                print("Election Date:",election_date_object) 
                print('Election Name = ',election_name)
                result_table = votebox.find_element(By.XPATH, ".//table[@class='results_table']")
                result_rows = result_table.find_elements(By.XPATH, ".//tr[contains(@class,'results_row')]")
                process = CrawlerProcess(get_project_settings())
                for result_row in result_rows:                    
                    candidate_url = result_row.find_element(By.XPATH, ".//td[@class='votebox-results-cell--text']//a").get_attribute('href').strip()
                    print('Candidate URL = ', candidate_url)
                    # candidate_info(candidate_url,election_name,election_date_object)
                    # CandidateInformation(candidate_url)
                    process.crawl(spc.CandidateInformation, candidate_url)
                    process.start()
                    break
                    try:
                        votes_percentage = result_row.find_element(By.XPATH, ".//td[@class='votebox-results-cell--number'][1]").text.strip()
                    except:
                        votes_percentage = '' 
                    print('Votes Percentage = ', votes_percentage)       
                    try:
                        votes_number = result_row.find_element(By.XPATH, ".//td[@class='votebox-results-cell--number'][2]").text.strip()
                    except:
                        votes_number = '' 
                    print('Votes Number = ', votes_number)       

            # break
        except:
            continue      

  

def candidate_info(candidate_url, election_name, election_date):
    # driver_candidate_info = webdriver.Chrome(service=serv_obj, options=options)
    # driver_candidate_info.maximize_window()    
    driver_candidate_info.get(candidate_url)
   
    info_box = driver_candidate_info.find_element(By.XPATH, "//div[@class='infobox person']")
    print("*"*70)
    name = info_box.find_element(By.XPATH, "./div[1]").text
    print("Name = ",name)
    photo_url = info_box.find_element(By.XPATH, "./div[2]//img").get_attribute('src')
    print('photo url = ', photo_url)
    party = info_box.find_element(By.XPATH, "./div[3]").text
    print("Party = ",party)

    try:
        incumbent = driver_candidate_info.find_element(By.XPATH,"//p[contains(.,'Incumbent:')]").text.split(':')[-1]
    except:
        incumbent = ''
    print("Incumbent = ",incumbent) 

    try:
        prior_office = info_box.find_element(By.XPATH, ".//div[contains(@class,'value-only') and contains(.,'Prior offices')]")
        prior_office_values = prior_office.find_elements(By.XPATH, ".//following-sibling::div[contains(@style,'font-weight: bold')]") 
        for prior_office_val in prior_office_values:
            print("prior office = ",prior_office_val.text)       
    except:
        prior_office = '' 
    # print("prior office = ", prior_office) 
    try:
        tenure = info_box.find_element(By.XPATH, ".//div[contains(.,'Tenure')]")
        current_office = tenure.find_element(By.XPATH, "./preceding-sibling::div[1]").text               
    except:
        current_office = ''  
    print("current_office = ", current_office) 
    try:
        education = info_box.find_element(By.XPATH, ".//div[contains(.,'Education')]")        
        education_infomaions = education.find_elements(By.XPATH, ".//following-sibling::div")
        for edu_info in education_infomaions:
            if 'value-only' in edu_info.get_attribute('class'):
                break
            else:
                print('Educaion = ', edu_info.text)
    except:
        print("Failed to find out education information.")  

    try:
        profession_key = info_box.find_element(By.XPATH, ".//div[(@class='widget-key') and contains(.,'Profession')]")
        print('profession key = ', profession_key.text)
        profession_val = profession_key.find_element(By.XPATH, ".//following-sibling::div[@class='widget-value'][1]").text
        print('Profession = ',profession_val)
    except:
        print('Profession value not found.')              

    try:
        contact_header = info_box.find_element(By.XPATH, ".//div[contains(@class,'value-only') and contains(.,'Contact')]")
        print('conact header = ', contact_header.text)
        contacts = contact_header.find_elements(By.XPATH, ".//following-sibling::div[contains(@class,'white')]//a")
               
        for contact in contacts:
            print(contact.text,' = ', contact.get_attribute('href'))
    except:
        print('contact information not found')
 
            



       
             

      
     
        
