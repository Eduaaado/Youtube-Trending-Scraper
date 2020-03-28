import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import matplotlib.pyplot as plt

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

def percent(n, total):
    return round((n/total)*100, 1)

categories = []
for link in videos:
    print('========================================')
    print('Getting categories ({}%)'.format(percent(videos.index(link)+1, len(videos))))
    try:
        c = getCategory(link)
        print(c)
        categories.append(c)
    except:
        pass

print('========================================')
print('Making data frame')
n = [1 for category in categories]
data = pd.DataFrame({"Category": categories, "n": n})
data = data.groupby('Category')['n'].sum()
data = data.to_frame()
data.reset_index(level=0, inplace=True)
data = data.sort_values(by='n', ascending=True)
print(data)

print('========================================')
print('Building chart')
fig1, chart = plt.subplots()
chart.pie(data['n'], labels=data['Category'], autopct='%1.1f%%', shadow=False, startangle=90)
chart.axis('equal')

plt.title('Youtube Trending Videos Categories')
print('~~~~~~~~~~~~~~~~~~~~')
print('-~ Done! ~-')
print('~~~~~~~~~~~~~~~~~~~~')
plt.show()