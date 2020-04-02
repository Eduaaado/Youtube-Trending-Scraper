from time import sleep
from time import perf_counter
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
sns.set()

# Dates info to use for file name later
date = datetime.datetime.now() # Gets current date
day = date.day # Gets day
month = date.month # Gets month
year = date.year # Gets year
hour = date.hour
minute = date.minute
if len(str(minute)) == 1: minute = '0'+str(minute)

# Function to find the category text
def findCat():
    showmore = driver.find_element_by_xpath('//*[@id="more"]/yt-formatted-string')
    driver.execute_script("arguments[0].click();", showmore)

    category = driver.find_element_by_xpath('//*[@id="content"]/yt-formatted-string/a')
    return category.get_attribute('innerHTML')
# Function to go to a video and find it's category
def getCategory(link): 
    print('========================================')
    print('Going to '+link)
    driver.get(link) # Go to video
    sleep(1) # Wait to load

    c = None
    try: # Tries to get it
        c = findCat()
    except: # If it fails, wait some seconds and try again
        try:
            sleep(3)
            c = findCat()
        except: 
            pass
    
    print(f'Getting categories ({percent(videos.index(link)+1, len(videos))}%)')
    return c

# Simple function to get percentage
def percent(n, total):
    return round((n/total)*100, 1)

tic = perf_counter()

driver = webdriver.Chrome(executable_path = 'tools/chromedriver') # Gets Chrome driver
driver.get('https://www.youtube.com/feed/trending') # Go to Youtube Trending page

print('Getting links')
videos = [thumb.get_attribute('href') for thumb in driver.find_elements_by_id('thumbnail') if thumb.get_attribute('href') != None]
print(f'All links listed! ({len(videos)})')

categories = [getCategory(link) for link in videos if not None]

driver.close()

# Create Data Frame
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

# Create chart
print('========================================')
print('Building chart')
mpl.rcParams['font.size'] = 9.0
fig1, chart = plt.subplots(constrained_layout=True)

cols = [
    '#FFDB15', '#3F5E98', '#918E80', '#2F2440', 
    '#01949A', '#F7BEC0', '#E7625F', '#02894B', 
    '#EAB996', '#C22660','#CFC1CE', '#9F2B00', 
    '#729663', '#9E3A14','#ed0000', '#2E3B51'
] # Set color palette

chart.pie(data['n'], shadow=False, startangle=90, colors=cols)
chart.axis('equal')

# Sets legend
percents = [percent(n, total) for n in data['n']]
plt.legend(labels=['%s, %1.1f %%' % (l, s) for l, s in zip(data['Category'], percents)], frameon=False, loc=2, bbox_to_anchor=(.94,.85))

centre_circle = plt.Circle((0,0),0.75,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.suptitle(f'Youtube Trending Categories ({hour}:{minute} on {day}/{month}/{year})')
toc = perf_counter()

totalsecs = toc - tic
minutes = int(totalsecs//60)
fmin = totalsecs/60
remain = float(str(fmin-int(fmin))[1:])
seconds = int(60*remain)
time = f'{minutes} minutes'
if seconds != 0: time = time+f' and {seconds} seconds'
print('~~~~~~~~~~~~~~~~~~~~')
print(f'-~ Done in {time}. ~-')
print('~~~~~~~~~~~~~~~~~~~~')


# Save figure file
fname = f'yt-trending-{day}-{month}-{year}.png'
print(f'Saving chart as {fname}')

plt.draw()
plt.savefig(fname, dpi=700)
plt.show()