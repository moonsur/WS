from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import csv


chrome_driver_path = 'C:\\data\\chromedriver\\chromedriver.exe'
serv_obj = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])



def scrape_video(video_url):
    driver_video =webdriver.Chrome(service=serv_obj, options=options)
    driver_video.maximize_window()
    driver_video.get(video_url)
    time.sleep(2)
    try:
        # description_box = driver_video.find_element(By.XPATH, "//ytd-text-inline-expander[@id='description-inline-expander']")
        description_box = WebDriverWait(driver_video, 10).until(EC.presence_of_element_located((By.XPATH, "//ytd-text-inline-expander[@id='description-inline-expander']")))    
        print(description_box.text)
    except TimeoutException:
        print("video description not located")
    driver_video.close()

driver = webdriver.Chrome(service=serv_obj, options=options)
driver.maximize_window()
url = "https://www.youtube.com/"
driver.get(url)
time.sleep(3)
driver.find_element(By.XPATH, "//input[@id='search']").send_keys("python tutorials")
try:   
    search_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='search-icon-legacy']")))
    search_btn.click()
except TimeoutException:
    print("search button not located")
time.sleep(1)
try:
    # button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='filter-menu']//a")))
    button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='filter-menu']//a")))
    button.click()
except TimeoutException:
    print("Failed to find filter button") 

driver.find_element(By.XPATH, "//a[contains(.,'View count')]").click()
time.sleep(2)

try:
    # videos = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//ytd-video-renderer[@bigger-thumbs-style='DEFAULT']")))
    videos = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//ytd-video-renderer[contains(@class,'style-scope ytd-item-section-renderer')]")))
   
    print(len(videos))
    cont = 0
    for video in videos:
        title = video.find_element(By.XPATH, ".//a[@id='video-title']")
        print(title.text)
        video_url = title.get_attribute("href")
        print(title.get_attribute("href"))
        scrape_video(video_url)
        if cont > 2:
            break
        cont += 1
        # views = video.find_element(By.XPATH, ".//div[@id='metadata-line']/span[1]")
        # print(views.text)
        # post_time = video.find_element(By.XPATH, ".//div[@id='metadata-line']/span[2]")
        # print(post_time.text)
        # chanel = video.find_element(By.XPATH, ".//yt-formatted-string[@id='text' and @class='style-scope ytd-channel-name']//a")
        # print(chanel.text)
        # print(chanel.get_attribute('href'))
    # video_list = [video.text for video in videos]
    # print(video_list)
except:
    print("video list finding failed")

