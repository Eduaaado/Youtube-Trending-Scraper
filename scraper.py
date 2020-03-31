import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
sns.set()

date = datetime.datetime.now()
day = date.day
month = date.month
year = date.year

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
total = sum(n)
data = pd.DataFrame({"Category": categories, "n": n})
data = data.groupby('Category')['n'].sum()
data = data.to_frame()
data.reset_index(level=0, inplace=True)
data = data.sort_values(by='n', ascending=True)
print(data) 

print('========================================')
print('Building chart')
mpl.rcParams['font.size'] = 9.0
fig1, chart = plt.subplots()

cols = sns.color_palette("cubehelix", 8)
chart.pie(data['n'], shadow=False, startangle=90, colors=cols)
chart.axis('equal')

percents = [percent(n, total) for n in data['n']]
plt.legend(labels=['%s, %1.1f %%' % (l, s) for l, s in zip(data['Category'], percents)], loc=2, bbox_to_anchor=(1,0.5))

centre_circle = plt.Circle((0,0),0.75,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title('Youtube Trending Videos Categories')
plt.tight_layout()
print('~~~~~~~~~~~~~~~~~~~~')
print('-~ Done! ~-')
print('~~~~~~~~~~~~~~~~~~~~')
plt.show()

fname = 'yt-trending-{}-{}-{}.png'.format(day, month, year)
print('Saving chart as {}'.format(fname))
plt.savefig(fname, dpi=700)