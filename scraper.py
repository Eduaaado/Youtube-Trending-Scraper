import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

driver = webdriver.Chrome(executable_path = 'tools/chromedriver')
driver.get('https://www.youtube.com/feed/trending')

def getCategory(link):
    print(link)
    driver.get(link)
    time.sleep(3)
    def getcat():
        showmore = driver.find_element_by_xpath('//*[@id="more"]/yt-formatted-string')
        driver.execute_script("arguments[0].click();", showmore)

        category = driver.find_element_by_xpath('//*[@id="content"]/yt-formatted-string/a')
        return category.get_attribute('innerHTML')

    try:
        c = getcat()
    except:
        time.sleep(5)
        c = getcat()
    
    return c

videos = []
for thumb in driver.find_elements_by_id('thumbnail'):
    videos.append(thumb.get_attribute('href'))
    print('Getting video links ({})'.format(len(videos)))
print('All links listed!')

#videos = videos[:5]

categories = []
for link in videos:
    print('========================================')
    print('Getting categories ({}%)'.format((int(videos.index(link)+1/len(videos)))))
    c = getCategory(link)
    print(c)
    categories.append(c)

n = [1 for category in categories]
data = pd.DataFrame(categories, n)
data.reset_index(level=0, inplace=True)
print(data)