import time
import requests
# from createtables import create_tables
# from insertUpdate import *
# import psycopg2
# from config import config
from datetime import datetime, timezone
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains




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

# driver_election_info = webdriver.Chrome(service=serv_obj, options=options)
# driver_election_info.maximize_window() 

# driver_candidate_info = webdriver.Chrome(service=serv_obj, options=options)
# driver_candidate_info.maximize_window()
all_candidate_urls = []
driver_election_info = None
driver_candidate_info = None 
total_urls = 0

def state_elections(all_state_urls):
    driver_by_state = webdriver.Chrome(service=serv_obj, options=options)
    driver_by_state.maximize_window() 

    all_us_senate_elections = []
    all_us_house_elections = []
    all_congress_special_elections = []
    congress_special_elections_urls = []
    all_governor_elections = []
    all_state_supreme_court_elections = []
    all_school_board_elections = []
    all_municipal_government_urls = []
    municipal_government_years = []
    all_state_executive_elections = []
    all_state_senate_elections = []
    all_state_house_elections = []
    global total_urls

    for state_info in all_state_urls:
        state_name = state_info[0]    
        election_year = state_info[1]    
        state_url = state_info[2]    
        driver_by_state.get(state_url)
        total_urls += 1
        
        all_elections = driver_by_state.find_elements(By.XPATH, "//table[@class='marqueetable']//a[not(contains(.,'Click here'))]")
    
        for election in all_elections:
            if election.text.strip().lower() == "u.s. senate":                           
                all_us_senate_elections.append((state_name, election_year, election.get_attribute('href').strip()))
            elif election.text.strip().lower() == "u.s. house":                           
                all_us_house_elections.append((state_name, election_year, election.get_attribute('href').strip())) 
            elif election.text.strip().lower() == "congress special election":
                if election.get_attribute('href').strip() not in congress_special_elections_urls:
                    all_congress_special_elections.append((state_name, election_year, election.get_attribute('href').strip()))
                    congress_special_elections_urls.append(election.get_attribute('href').strip()) 
            elif election.text.strip().lower() == "governor":                           
                all_governor_elections.append((state_name, election_year, election.get_attribute('href').strip()))        
            elif election.text.strip().lower() == "other state executive":                           
                all_state_executive_elections.append((state_name, election_year, election.get_attribute('href').strip()))        
            elif election.text.strip().lower() == "state senate":                           
                all_state_senate_elections.append((state_name, election_year, election.get_attribute('href').strip()))        
            elif election.text.strip().lower() == "state house":                           
                all_state_house_elections.append((state_name, election_year, election.get_attribute('href').strip()))        
            elif election.text.strip().lower() == "state supreme court":                           
                all_state_supreme_court_elections.append((state_name, election_year, election.get_attribute('href').strip()))        
            elif election.text.strip().lower() == "school boards":                           
                all_school_board_elections.append((state_name, election_year, election.get_attribute('href').strip()))        
            elif election.text.strip().lower() == "municipal government":
                if election_year not in municipal_government_years:                           
                    all_municipal_government_urls.append((state_name, election_year, election.get_attribute('href').strip())) 
                    municipal_government_years.append(election_year)       


    driver_by_state.close()
    
    # print("************** U.S. Senate *******************")
    # print(*all_us_senate_elections,sep='\n')
    # print("************** U.S. House *******************")
    # print(*all_us_house_elections,sep='\n')
    # print("************** Congress special election *******************")
    # print(*all_congress_special_elections,sep='\n')
    # print("************** Governor election *******************")
    # print(*all_governor_elections,sep='\n')
    # print("************** School board election *******************")
    # print(*all_school_board_elections,sep='\n')
    # print("************** Municipal Government election *******************")
    # print(*all_municipal_government_urls,sep='\n')
    # print("************** Other state executive election *******************")
    # print(*all_state_executive_elections,sep='\n')
    # print("************** state senate election *******************")
    # print(*all_state_senate_elections,sep='\n')
    print("************** state house election *******************")
    print(*all_state_house_elections,sep='\n')

    global driver_election_info 
    driver_election_info = webdriver.Chrome(service=serv_obj, options=options)
    driver_election_info.maximize_window() 

    global driver_candidate_info
    driver_candidate_info = webdriver.Chrome(service=serv_obj, options=options)
    driver_candidate_info.maximize_window() 

    # us_senate(all_us_senate_elections)
    # us_house(all_us_house_elections)
    # congress_special_election(all_congress_special_elections)
    # governor(all_governor_elections)
    # state_supreme_court(all_state_supreme_court_elections)
    # school_boards(all_school_board_elections)
    # municipal_government(all_municipal_government_urls)
    # state_executive(all_state_executive_elections)
    state_senate(all_state_senate_elections)
    # state_house(all_state_house_elections)

    print('Total Urls Scraped = ', total_urls)
    



def us_senate(all_us_senate_elections):  
    # global driver_candidate_info
    # driver_candidate_info = webdriver.Chrome(service=serv_obj, options=options)
    # driver_candidate_info.maximize_window()
    global total_urls   
    for senate_election in all_us_senate_elections:
        state_name = senate_election[0]
        election_year = senate_election[1]
        election_url = senate_election[2]
        driver_election_info.get(election_url) 
        total_urls += 1    
        # voteboxes = driver_election_info.find_elements(By.XPATH, "//div[@class='votebox']")
        xp = f"//div[@class='votebox' and .//p[contains(.,'{election_year}')]]"            
        voteboxes = driver_election_info.find_elements(By.XPATH, xp)         

        scrape_voteboxes(state_name, election_year, voteboxes)
        


def us_house(all_us_house_elections):
    # driver_election_info = webdriver.Chrome(service=serv_obj, options=options)
    # driver_election_info.maximize_window() 
    global total_urls
   
    for house_election in all_us_house_elections:
        state_name = house_election[0]
        election_year = house_election[1]
        election_url = house_election[2]
        driver_election_info.get(election_url)
        total_urls += 1       
        # voteboxes = driver_election_info.find_elements(By.XPATH, "//div[@class='votebox']")  
        xp = f"//div[@class='votebox' and .//p[contains(.,'{election_year}')]]"            
        voteboxes = driver_election_info.find_elements(By.XPATH, xp)  
        if len(voteboxes) > 0:      
            scrape_voteboxes(state_name, election_year, voteboxes)             
        else:
            district_election_urls = driver_election_info.find_elements(By.XPATH, "//h3[contains(.,'District') and ./span[contains(@id,'District')]]/following-sibling::dl[1]//a")
            lst_district_election_urls = [dis_ele_url.get_attribute('href').strip() for dis_ele_url in district_election_urls]
            print('Number of District = ',len(lst_district_election_urls))
            # cont = 1
            for district_election_url in lst_district_election_urls:
                driver_election_info.get(district_election_url)
                xp = f"//div[@class='votebox' and .//p[contains(.,'{election_year}')]]"
                print(xp)
                voteboxes = driver_election_info.find_elements(By.XPATH, xp)    
                if len(voteboxes) > 0:      
                    print('voteboxes lenght for district election = ',len(voteboxes))
                    scrape_voteboxes(state_name, election_year, voteboxes)
                # if cont > 5:
                #     break
                # cont +=1

def congress_special_election(all_congress_special_elections):
    # driver_election_info = webdriver.Chrome(service=serv_obj, options=options)
    # driver_election_info.maximize_window() 
    global total_urls
    scraped_urls = []
    for congress_special_election in all_congress_special_elections:
        state_name = congress_special_election[0]
        election_year = congress_special_election[1]
        election_url = congress_special_election[2]
        if election_url not in scraped_urls:
            driver_election_info.get(election_url) 
            total_urls += 1      
            # voteboxes = driver_election_info.find_elements(By.XPATH, "//div[@class='votebox']")
            xp = f"//div[@class='votebox' and .//p[contains(.,'{election_year}')]]"            
            voteboxes = driver_election_info.find_elements(By.XPATH, xp)     
            if len(voteboxes) > 0:      
                scrape_voteboxes(state_name, election_year, voteboxes) 
                scraped_urls.append(congress_special_election)           
            else:
                xp_se =f"//ul/li/a[contains(@title,'special') and contains(@href,'{election_year}')]"              
                special_elections = driver_election_info.find_elements(By.XPATH, xp_se)
                
                lst_special_election_urls = [spc_ele_url.get_attribute('href').strip() for spc_ele_url in special_elections if spc_ele_url.get_attribute('href').strip() not in scraped_urls]
                print('Number of special election = ',len(lst_special_election_urls))            
                for special_election_url in lst_special_election_urls:
                    if special_election_url not in scraped_urls:
                        driver_election_info.get(special_election_url)
                        total_urls += 1
                        xp = f"//div[@class='votebox' and .//p[contains(.,'{election_year}')]]"
                        print(xp)
                        voteboxes = driver_election_info.find_elements(By.XPATH, xp)    
                        if len(voteboxes) > 0:      
                            print('voteboxes lenght for district election = ',len(voteboxes))
                            scrape_voteboxes(state_name, election_year, voteboxes)
                        
                        scraped_urls.append(special_election_url)

    print("Scraped Urls: ")  
    print(*scraped_urls, sep='\n')              


def governor(all_governor_elections): 
    global total_urls      
    for governor_election in all_governor_elections:
        state_name = governor_election[0]
        election_year = governor_election[1]
        election_url = governor_election[2]
        driver_election_info.get(election_url) 
        total_urls += 1    
        # voteboxes = driver_election_info.find_elements(By.XPATH, "//div[@class='votebox']")
        xp = f"//div[@class='votebox' and .//p[contains(.,'{election_year}')]]"            
        voteboxes = driver_election_info.find_elements(By.XPATH, xp)         

        scrape_voteboxes(state_name, election_year, voteboxes)

def state_senate(all_state_senate_elections):           
    for state_senate_election in all_state_senate_elections:
        state_name = state_senate_election[0]
        election_year = state_senate_election[1]
        election_url = state_senate_election[2]
        office = 'State Senate'

        scrape_headertabs(state_name, election_year, election_url, office) 

def state_house(all_state_house_elections):           
    for state_house_election in all_state_house_elections:
        state_name = state_house_election[0]
        election_year = state_house_election[1]
        election_url = state_house_election[2]
        office = 'State House'

        scrape_headertabs(state_name, election_year, election_url, office)        

        
def scrape_headertabs(state_name, election_year, election_url, office):
    global total_urls
    global all_candidate_urls
    driver_election_info.get(election_url)
    total_urls += 1

    general_election_date_obj = None
    primary_election_date_obj = None
    primary_runoff_election_date_obj = None

    election_date_rows = driver_election_info.find_elements(By.XPATH, "//table[@class='infobox']//tr[./td[./b[contains(.,'Primary') or contains(.,'Primary runoff') or contains(.,'General')]]]")
    
    if len(election_date_rows) > 0:        
        for election_date_row in election_date_rows:
            if 'General' in election_date_row.find_element(By.XPATH, "./td[1]").text:
                general_election_date_str = election_date_row.find_element(By.XPATH, "./td[2]").text.strip()
                # print('General: ', general_election_date_str) 
                general_election_date_obj = datetime.strptime(general_election_date_str, "%B %d, %Y")
                # print('General Date Obj: ', general_election_date_obj)    
            elif 'Primary' in election_date_row.find_element(By.XPATH, "./td[1]").text and 'Primary runoff' not in election_date_row.find_element(By.XPATH, "./td[1]").text:
                primary_election_date_str = election_date_row.find_element(By.XPATH, "./td[2]").text.strip()
                # print('Primary: ', primary_election_date_str)
                primary_election_date_obj = datetime.strptime(primary_election_date_str, "%B %d, %Y")
                # print('Primary Date obj: ', primary_election_date_obj)     
            elif 'Primary runoff' in election_date_row.find_element(By.XPATH, "./td[1]").text:
                primary_runoff_election_date_str = election_date_row.find_element(By.XPATH, "./td[2]").text.strip()
                # print('Primary runoff: ', primary_runoff_election_date_str)
                primary_runoff_election_date_obj = datetime.strptime(primary_runoff_election_date_str, "%B %d, %Y")
                # print('Primary runoff date obj: ', primary_runoff_election_date_obj)

#************* General Elections Section *******************
    try:
        general = driver_election_info.find_element(By.XPATH, "//div[@id='General']")
        general_election_of_sub_offices = general.find_elements(By.XPATH, ".//tbody/tr")[3:]
        
        general_election_name_prefix = "General election for " + office + " " + state_name
        
        print('*'*50)
        print("General Election Date: ",general_election_date_obj)
        for general_election_of_sub_office in general_election_of_sub_offices:
            tds = general_election_of_sub_office.find_elements(By.XPATH, "./td")
            sub_office = tds[0].text.strip()
            general_election_name = general_election_name_prefix + " " + sub_office
            candidate_urls = []
            incumbents = [] 
        
            for i in range(1,4):
                    try:
                        for candidate_span in tds[i].find_elements(By.XPATH, ".//span[@class='candidate']"):
                            candidate_urls.append(candidate_span.find_element(By.XPATH, ".//a[not (./img)]").get_attribute('href')) 
                            print('Candidate Text', candidate_span.text)
                            if '(i)' in candidate_span.text:
                                incumbents.append('Yes')
                            else:
                                incumbents.append('')                
                    except:
                        print(f"{office} - {sub_office} General Election, somthing went wrong into candidate collection on column : ", i)
            print('Office = ', office)
            print('Sub Office = ', sub_office) 
            print('Election Name : ', general_election_name)        
            print('Incumbents : ', incumbents)        
            print('Candidate Urls : ', candidate_urls)
            for i in range(len(candidate_urls)):
                if candidate_urls[i] in all_candidate_urls:
                    print("@@@@@@@@@@@@ This Candidate is already in List @@@@@@@@@@@ ")
                else: 
                    candidate_info(candidate_urls[i], general_election_name, general_election_date_obj, incumbents[i])
                    all_candidate_urls.append(candidate_urls[i])        
    except:
        print(f"Something went wrong in {office} General and url is = {election_url}")
# **************** Primary runoff elections Section *********************
    # time.sleep(2)
    try:
        driver_election_info.find_element(By.XPATH, "//div[@id='headertabs']//a[@href='#Primary_runoff']").click()  
        primary_runoff = driver_election_info.find_element(By.XPATH, "//div[@id='Primary_runoff']") 
        primary_runoff_election_of_sub_offices = primary_runoff.find_elements(By.XPATH, ".//tbody/tr")[3:]    
        # general_election_name_prefix = "General election for " + office + " " + state_name
        print('*'*50)
        print("Primary Runoff Election Date: ",primary_runoff_election_date_obj)
        for primary_runoff_election_of_sub_office in primary_runoff_election_of_sub_offices:
            tds = primary_runoff_election_of_sub_office.find_elements(By.XPATH, "./td")
            sub_office = tds[0].text.strip()           
                        
            for i in range(1,3):
                candidate_urls = []
                incumbents = [] 
                try:
                    for candidate_span in tds[i].find_elements(By.XPATH, ".//span[@class='candidate']"):
                        candidate_urls.append(candidate_span.find_element(By.XPATH, ".//a[not (./img)]").get_attribute('href')) 
                        if i == 1:
                            primary_runoff_election_name = "Democratic primary runoff for " +  office + " " + state_name + " " + sub_office 
                        elif i == 2:
                            primary_runoff_election_name = "Republican primary runoff for " +  office + " " + state_name  + " " + sub_office   
                        print('Candidate Text', candidate_span.text)
                        if '(i)' in candidate_span.text:
                            incumbents.append('Yes')
                        else:
                            incumbents.append('')  
                    if len(candidate_urls) > 0:
                        print('*=*'*15)
                        print('Candidate urls len : ', len(candidate_urls))
                        print('i = ',i)
                        print('Office = ', office)
                        print('Sub Office = ', sub_office)        
                        print('Election Name : ', primary_runoff_election_name)        
                        print('Incumbents : ', incumbents)        
                        print('Candidate Urls : ', candidate_urls)
                        for i in range(len(candidate_urls)):
                            if candidate_urls[i] in all_candidate_urls:
                                print("@@@@@@@@@@@@ This Candidate is already in List @@@@@@@@@@@ ")
                            else: 
                                candidate_info(candidate_urls[i], primary_runoff_election_name, primary_runoff_election_date_obj, incumbents[i])
                                all_candidate_urls.append(candidate_urls[i])

                except:
                    print("Primary runoff Election, somthing went wrong into candidate collection on column : ", i)
    except:        
        print(f"Something went wrong in {office} Primary runoff and url is = {election_url}")  
    
# **************** Primary elections Section *********************

    try:
        driver_election_info.find_element(By.XPATH, "//div[@id='headertabs']//a[@href='#Primary']").click()  
        primary = driver_election_info.find_element(By.XPATH, "//div[@id='Primary']") 
        primary_election_of_sub_offices = primary.find_elements(By.XPATH, ".//tbody/tr")[3:]    
       
        print('*'*50)
        print("Primary Election Date: ", primary_election_date_obj)
        for primary_election_of_sub_office in primary_election_of_sub_offices:
            tds = primary_election_of_sub_office.find_elements(By.XPATH, "./td")
            sub_office = tds[0].text.strip()            
           
            for i in range(1,3):
                candidate_urls = []
                incumbents = [] 
                try:
                    for candidate_span in tds[i].find_elements(By.XPATH, ".//span[@class='candidate']"):
                        candidate_urls.append(candidate_span.find_element(By.XPATH, ".//a[not (./img)]").get_attribute('href')) 
                        if i == 1:
                            primary_election_name = "Democratic primary for " +  office + " " + state_name + " " + sub_office 
                        elif i == 2:
                            primary_election_name = "Republican primary for " +  office + " " + state_name  + " " + sub_office   
                        print('Candidate Text', candidate_span.text)
                        if '(i)' in candidate_span.text:
                            incumbents.append('Yes')
                        else:
                            incumbents.append('')
                    if len(candidate_urls) > 0:
                        print('*=*'*15)
                        print('Office = ', office)
                        print('Sub Office = ', sub_office)        
                        print('Election Name : ', primary_election_name)        
                        print('Incumbents : ', incumbents)        
                        print('Candidate Urls : ', candidate_urls)
                        for i in range(len(candidate_urls)):
                            if candidate_urls[i] in all_candidate_urls:
                                print("@@@@@@@@@@@@ This Candidate is already in List @@@@@@@@@@@ ")
                            else: 
                                candidate_info(candidate_urls[i], primary_election_name, primary_election_date_obj, incumbents[i])
                                all_candidate_urls.append(candidate_urls[i])        
                except:
                    print("Primary Election, somthing went wrong into candidate collection on column : ", i)                
    except:        
        print(f"Something went wrong in {office} Primary and url is = {election_url}") 

def state_executive(all_state_executive_elections):
    global total_urls 
    global all_candidate_urls   
    all_state_executive_election_urls = []       
    state_executive_election_urls_only = []       
    for state_executive_election in all_state_executive_elections:
        state_name = state_executive_election[0]
        election_year = state_executive_election[1]
        election_url = state_executive_election[2]
        driver_election_info.get(election_url)
        total_urls += 1     
        state_executive_elections = driver_election_info.find_elements(By.XPATH, "//table[@class='infobox']/following-sibling::p[2]//a[not (text()='Governor')]")
        for state_executive_election in state_executive_elections:
            if state_executive_election.get_attribute('href') not in state_executive_election_urls_only:
                title = state_executive_election.text
                url = state_executive_election.get_attribute('href')
                all_state_executive_election_urls.append((state_name, election_year, title, url))
                state_executive_election_urls_only.append(url)

    print("State executive election urls:")
    print("^"*50)
    print(*all_state_executive_election_urls,sep='\n')
    for state_executive_election_url in all_state_executive_election_urls:
        print("State executive election url:")
        print("^"*50)
        print(state_executive_election_url)
        state_name_se = state_executive_election_url[0]
        election_year_se = state_executive_election_url[1]
        election_title_se = state_executive_election_url[2]
        election_url_se = state_executive_election_url[3]
        driver_election_info.get(election_url_se)
        total_urls += 1
        # try:
        #     show = driver_election_info.find_element(By.XPATH,"//div[@class='all-content']//a[@class='ShowThis' and contains(.,'Show more')]")
        #     print(show.text)
        #     action = ActionChains(driver_election_info) 
        #     action.click(on_element = show)
        #     action.perform()
        # except:
        #     pass 
        
        xp = f"//div[@class='votebox' and .//p[contains(.,'{election_year_se}')]]"            
        voteboxes = driver_election_info.find_elements(By.XPATH, xp)
        final_voteboxes = []         
        if len(voteboxes) > 0:
            for votebox in voteboxes:
                if election_title_se.lower() in votebox.find_element(By.XPATH, ".//h5[@class='votebox-header-election-type']").text.lower():
                    final_voteboxes.append(votebox)

            if len(final_voteboxes) > 0:
                scrape_voteboxes(state_name, election_year, final_voteboxes)
                pass
        else:
            general_election_date_obj = None
            primary_election_date_obj = None
            primary_runoff_election_date_obj = None
            elections_date = driver_election_info.find_elements(By.XPATH, "//table[@class='infobox']//td/small[./b[contains(.,'Primary') or contains(.,'Primary runoff') or contains(.,'General')]]")
            if len(elections_date) > 0:
                for election_date in elections_date:
                    if 'General:' in election_date.text:
                        general_election_date_str = str.replace(election_date.text.split(':')[-1],"(canceled)",'').strip()
                        print('General: ', general_election_date_str) 
                        general_election_date_obj = datetime.strptime(general_election_date_str, "%B %d, %Y")   
                    elif 'Primary:' in election_date.text:
                        primary_election_date_str = str.replace(election_date.text.split(':')[-1],"(canceled)",'').strip()
                        print('Primary: ', primary_election_date_str)
                        primary_election_date_obj = datetime.strptime(primary_election_date_str, "%B %d, %Y")     
                    elif 'Primary runoff:' in election_date.text:
                        primary_runoff_election_date_str = str.replace(election_date.text.split(':')[-1],"(canceled)",'').strip()
                        print('Primary runoff: ', primary_runoff_election_date_str)
                        primary_runoff_election_date_obj = datetime.strptime(primary_runoff_election_date_str, "%B %d, %Y")     

            sub_offices = driver_election_info.find_elements(By.XPATH, "//h2[./span[@id='Candidates_and_election_results']]//following-sibling::h3[./span[contains(@class,'mw-headline') and not (starts-with(@id,'20')) and not (starts-with(@id,'Campaign'))]]")
            if len(sub_offices) > 0:
                for sub_office in sub_offices:
                    election_title = ''
                    sub_office_name = sub_office.text.strip()
                    print("Sub Offices : ", sub_office_name)
                    sub_office_siblings = sub_office.find_elements(By.XPATH, "./following-sibling::*")
                    flag = 0
                    sub_election_name = ''                                       
                    election_date_obj = None
                 
                    for sub_office_sibling in sub_office_siblings:                        
                        # if sub_office_sibling.tag_name == 'h3' or sub_office_sibling.tag_name == 'h2':
                        if sub_office_sibling.tag_name == 'h2' or sub_office_sibling.tag_name == 'h3' or sub_office_sibling.tag_name == 'h4':
                            break
                        elif sub_office_sibling.tag_name == 'p':
                            if flag == 0:
                                try:
                                    sub_election_text = sub_office_sibling.find_element(By.XPATH, "./span[contains(@style,'font-weight: bold')]")
                                except:
                                    continue
                                if election_title_se != "University of Michigan Board of Regents":    
                                    sub_election_name = str.replace(sub_election_text.text,'candidates', '').strip() + ' for ' + state_name_se +' '+ election_title_se +' '+ sub_office.text.strip()
                                    election_title = election_title_se
                                else:
                                     sub_election_name = str.replace(sub_election_text.text,'candidates', '').strip() + ' for ' + sub_office.text.strip()
                                     if election_title == '': 
                                        election_title = sub_office_name
                                        sub_office_name = ''

                                if 'general' in sub_election_name.lower():
                                    election_date_obj = general_election_date_obj
                                elif 'primary runoff' in sub_election_name.lower():
                                    election_date_obj = primary_runoff_election_date_obj
                                else:
                                    election_date_obj = primary_election_date_obj        
                                # print("Election Name : ",sub_election_name)
                                flag = 1
                                #General election for Alabama State Board of Education District 1
                            elif flag == 1:
                                if sub_office_sibling.text == '':
                                    flag = 2
                                    
                        elif sub_office_sibling.tag_name == 'ul':
                            if flag == 2:
                                candidates_li = sub_office_sibling.find_elements(By.XPATH, ".//li")
                                candidate_urls = []
                                incumbents = [] 
                                for candidate_li in candidates_li:
                                    if 'incumbent' in candidate_li.text.strip().lower():
                                        incumbents.append('Yes')
                                    else:
                                        incumbents.append('')    
                                    try:    
                                        candidate_url = candidate_li.find_element(By.XPATH, "./a").get_attribute('href')
                                        candidate_urls.append(candidate_url)
                                    except:
                                        continue 
                                
                                flag = 0 
                                print("**************** Sub office Elelction Details ***************")    
                                print('Election Title: ', election_title)
                                print('Sub Office Name: ', sub_office_name)
                                print("Election Date: ",election_date_obj) 
                                print('Election Name: ',sub_election_name)
                                print('Incumbents: ', incumbents)
                                print('Candidate Urls: ', candidate_urls)
                                for i in range(len(candidate_urls)):
                                    if candidate_urls[i] in all_candidate_urls:
                                        print("@@@@@@@@@@@@ This Candidate is already in List @@@@@@@@@@@ ")
                                    else: 
                                        candidate_info(candidate_urls[i], sub_election_name, election_date_obj, incumbents[i])
                                        all_candidate_urls.append(candidate_urls[i])
                            
                            else:
                                flag = 0
                            

                            # print("Tag Text : ", sub_office_sibling.text)
                        else:
                            print("Tag name : ", sub_office_sibling.tag_name)
            else:
                candidates_and_election_results_siblings = driver_election_info.find_elements(By.XPATH, "//h2[./span[@id='Candidates_and_election_results']]/following-sibling::*")
                flag = 0
                election_name = ''                                       
                election_date_obj = None
                sub_office_name = ''
                
                for candidates_and_election_results_sibling in candidates_and_election_results_siblings: 
                    if candidates_and_election_results_sibling.tag_name == 'h2' or candidates_and_election_results_sibling.tag_name == 'h3' or candidates_and_election_results_sibling.tag_name == 'h4':
                        break
                    elif candidates_and_election_results_sibling.tag_name == 'p':
                        if flag == 0:
                            try:
                                election_text = candidates_and_election_results_sibling.find_element(By.XPATH, "./span[contains(@style,'font-weight: bold')]")
                            except:
                                continue
                              
                            election_name = str.replace(election_text.text,'candidates', '').strip() + ' for ' + state_name_se +' '+ election_title_se
                            election_title = election_title_se
                            
                            if 'general' in election_name.lower():
                                election_date_obj = general_election_date_obj
                            elif 'primary runoff' in election_name.lower():
                                election_date_obj = primary_runoff_election_date_obj
                            else:
                                election_date_obj = primary_election_date_obj        
                            # print("Election Name : ",sub_election_name)
                            flag = 1
                            #General election for Alabama State Board of Education District 1
                        elif flag == 1:
                            if candidates_and_election_results_sibling.text == '':
                                flag = 2
                                
                    elif candidates_and_election_results_sibling.tag_name == 'ul':
                        if flag == 2:
                            candidates_li = candidates_and_election_results_sibling.find_elements(By.XPATH, ".//li")
                            candidate_urls = []
                            incumbents = [] 
                            for candidate_li in candidates_li:
                                if 'incumbent' in candidate_li.text.strip().lower():
                                    incumbents.append('Yes')
                                else:
                                    incumbents.append('')    
                                try:    
                                    candidate_url = candidate_li.find_element(By.XPATH, "./a").get_attribute('href')
                                    candidate_urls.append(candidate_url)
                                except:
                                    continue 
                            
                            flag = 0 
                            print("**************** Elelction Details ***************")    
                            print('Election Title: ', election_title)
                            print('Sub Office Name: ', sub_office_name)
                            print("Election Date: ",election_date_obj) 
                            print('Election Name: ',election_name)
                            print('Incumbents: ', incumbents)
                            print('Candidate Urls: ', candidate_urls)
                            for i in range(len(candidate_urls)):
                                if candidate_urls[i] in all_candidate_urls:
                                    print("@@@@@@@@@@@@ This Candidate is already in List @@@@@@@@@@@ ")
                                else: 
                                    candidate_info(candidate_urls[i], election_name, election_date_obj, incumbents[i])
                                    all_candidate_urls.append(candidate_urls[i])
                        
                        else:
                            flag = 0

                    else:
                        print("Tag name : ", candidates_and_election_results_sibling.tag_name)


def school_boards(all_school_board_elections):
    global total_urls  
    all_school_board_election_urls = [] 
    for school_board_election in all_school_board_elections:
        state_name = school_board_election[0]
        election_year = school_board_election[1]
        election_url = school_board_election[2]
        driver_election_info.get(election_url)
        total_urls += 1
        school_board_election_link_tags = driver_election_info.find_elements(By.XPATH,"//div[@id='Elections']/div[@class='scrollable-table-container']//tbody//a")
        for school_board_election_link_tag in school_board_election_link_tags:
            url = school_board_election_link_tag.get_attribute('href')
            all_school_board_election_urls.append((state_name, election_year, url))
            
    print("School board election urls:")
    print("^"*50)
    print(*all_school_board_election_urls, sep='\n')
    for school_board_election_url in all_school_board_election_urls:
        state_name_sb = school_board_election_url[0]
        election_year_sb = school_board_election_url[1]
        election_url_sb = school_board_election_url[2]
        driver_election_info.get(election_url_sb)
        total_urls += 1

        # voteboxes = driver_election_info.find_elements(By.XPATH, "//div[@class='votebox']")  
        xp = f"//div[@class='votebox' and .//p[contains(.,'{election_year_sb}')]]"            
        voteboxes = driver_election_info.find_elements(By.XPATH, xp)  
        if len(voteboxes) > 0:      
            scrape_voteboxes(state_name_sb, election_year_sb, voteboxes) 


def municipal_government(all_municipal_government_urls): 
    global total_urls

    all_municipal_government_election_urls = [] 
    for municipal_government_url in all_municipal_government_urls:
        # state_name = municipal_government_url[0]
        election_year = municipal_government_url[1]
        election_url = municipal_government_url[2]
        driver_election_info.get(election_url)
        total_urls += 1
        all_state_h3 = driver_election_info.find_elements(By.XPATH,"//div[@id='By_state']//h3")
        for state_h3 in all_state_h3:
            state_name = state_h3.text
            try:
                state_ul = state_h3.find_element(By.XPATH,"./following-sibling::ul")
                municipal_government_election_urls_by_state = state_ul.find_elements(By.XPATH, ".//a")
                for municipal_government_election_url in municipal_government_election_urls_by_state:
                    url = municipal_government_election_url.get_attribute('href')
                    all_municipal_government_election_urls.append((state_name, election_year, url))
            except:
                pass
     
            
    print("Municipal government election urls:")
    print("$"*50)
    print(*all_municipal_government_election_urls, sep='\n')
    for municipal_government_election_url in all_municipal_government_election_urls:
        state_name_mg = municipal_government_election_url[0]
        election_year_mg = municipal_government_election_url[1]
        election_url_mg = municipal_government_election_url[2]
        driver_election_info.get(election_url_mg)
        total_urls += 1

        # voteboxes = driver_election_info.find_elements(By.XPATH, "//div[@class='votebox']")  
        xp = f"//div[@class='votebox' and .//p[contains(.,'{election_year_mg}')]]"            
        voteboxes = driver_election_info.find_elements(By.XPATH, xp)  
        if len(voteboxes) > 0:      
            scrape_voteboxes(state_name_mg, election_year_mg, voteboxes)             
              
#*************** Not completed, will do later *********************
def state_supreme_court(all_state_supreme_court_elections):       
    for state_supreme_court_election in all_state_supreme_court_elections:
        state_name = state_supreme_court_election[0]
        election_year = state_supreme_court_election[1]
        election_url = state_supreme_court_election[2]
        driver_election_info.get(election_url) 
       
        places = driver_election_info.find_elements(By.XPATH, "//h3[contains(.,'Place') or contains(.,'Position')]")
        print('No of places: ',len(places))
        if len(places) > 0:
            for place in places:
                all_siblings_of_place = place.find_elements(By.XPATH, "./following-sibling::* ")
                print(f'place name: {place.text}, Length of all sibling: {len(all_siblings_of_place)}')
                print('place name:',place.text,', Tag name: ',place.tag_name)
                for sibling_of_place in all_siblings_of_place:
                    if sibling_of_place.tag_name == 'h2' or sibling_of_place.tag_name == 'h3':
                        break
                    elif sibling_of_place.tag_name == 'div' and 'votebox-scroll-container' in sibling_of_place.get_attribute('class'):
                        print('The votebox parent container') 
                        xp = f".//div[@class='votebox' and .//p[contains(.,'{election_year}')]]"            
                        voteboxes = sibling_of_place.find_elements(By.XPATH, xp) 
                        print("lenght of voteboxes: ", len(voteboxes))        

                        scrape_voteboxes(state_name, election_year, voteboxes)

def scrape_voteboxes(state_name, election_year, voteboxes):
    print('Into the scrape voteboxes')
    global all_candidate_urls
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
                    try:                    
                        candidate_url = result_row.find_element(By.XPATH, ".//td[@class='votebox-results-cell--text']//a").get_attribute('href').strip()
                        print('Candidate URL = ', candidate_url)
                        if candidate_url in all_candidate_urls:
                            print("@@@@@@@@@@@@ This Candidate is already in List @@@@@@@@@@@ ")
                        else:
                            candidate_info(candidate_url,election_name,election_date_object)
                            all_candidate_urls.append(candidate_url)
                    except:
                        continue        
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
        except Exception as e:
            print("Someting went wrong in scrape_voteboxes") 
            print(e)     

  

def candidate_info(candidate_url, election_name, election_date, incumbent = ''):
    global total_urls
    print("%%%%%%%%%%%%%%%%%%%% Inside Candidate Info %%%%%%%%%%%%%%%%")
    # driver_candidate_info = webdriver.Chrome(service=serv_obj, options=options)
    # driver_candidate_info.maximize_window()    
    driver_candidate_info.get(candidate_url)
    total_urls += 1
   
    info_box = driver_candidate_info.find_element(By.XPATH, "//div[@class='infobox person']")
    print("*"*70)
    name = info_box.find_element(By.XPATH, "./div[1]").text
    print("Name = ",name)
    photo_url = info_box.find_element(By.XPATH, "./div[2]//img").get_attribute('src')
    print('photo url = ', photo_url)
    party = info_box.find_element(By.XPATH, "./div[3]").text
    print("Party = ",party)
    if incumbent == '':
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
    
    educations = info_box.find_elements(By.XPATH, ".//div[contains(.,'Education') and contains(@class,'widget-row value-only')]")
    if len(educations) > 0:
        for education in educations:
            if education.text.strip().lower() == 'education':
                education_infomaions = education.find_elements(By.XPATH, ".//following-sibling::div")
                for edu_info in education_infomaions:
                    if 'value-only' in edu_info.get_attribute('class'):
                        break
                    else:
                        print('Educaion = ', edu_info.text)
            else:
                 print('Education information not found!')             
    else:
        print('Education information not found!')  

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
 
 