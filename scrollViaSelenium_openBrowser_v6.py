from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import time

from optparse import OptionParser
from matplotlib.cbook import dedent
from requests_testadapter import Resp
import requests
import os
import re
import json
import pickle
from lxml import html

import codecs
import csv


class SessionRemote(webdriver.Remote):
    def start_session(self, desired_capabilities, browser_profile=None):
        # Skip the NEW_SESSION command issued by the original driver
        # and set only some required attributes
        self.w3c = True
        
#export PATH=$PATH:~/anaconda/gecko_selenium/

profile = webdriver.FirefoxProfile()
profile.set_preference("permissions.default.image", 2)
#driver = webdriver.Firefox(firefox_profile=profile)


#url = "http://127.0.0.1:60749"
session_id = "c0a5f283-97f9-0743-b5ca-172409e94c1d"

url = "http://127.0.0.1:61041"
session_id = "9b60f749-d5ef-d94d-9dd0-c15a75bec292"

#driver = webdriver.Remote(command_executor=url,firefox_profile=profile)
#driver.session_id = session_id
#new RemoteWebDriver(new URL("http://localhost:7055/hub"),capabilities);
#driver = new RemoteWebDriver(new URL(url),firefox_profile=profile);

driver = SessionRemote(command_executor=url,desired_capabilities={})
driver.session_id = session_id



## 15 May 2019
## Shortlisted Apps
#1.Cashe
#driver.get("https://play.google.com/store/apps/details?id=co.tslc.cashe.android&showAllReviews=true")
# 2. Early Salary
#driver.get("https://play.google.com/store/apps/details?id=com.earlysalary.android&showAllReviews=true")
#appname= "earlysalary"

wait = WebDriverWait(driver, 10)
SCROLL_PAUSE_TIME = 0.5

#Whandles = driver.window_handles
#print(Whandles)

# Changer order to Newest First
#driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/c-wiz/div/div").click()
#time.sleep(3)

# click newest here.
#driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/c-wiz/div[1]/div/div[2]/div[1]").click()
#time.sleep(1)

   

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# Counter for number of reviews scraped:
k = 40

for i in range(1):

    print(i)
    #scroll till you see 'show more'
    for j in range(5):
        print('in inner loop')
        for n in range(40):
            
            username_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k+1) + "]/div/div[2]/div[1]/div[1]/span")            
            
            try:
                username =  driver.find_element_by_xpath(username_pth).text
            except NoSuchElementException as exception: 
                print("error")
                break
            else:
                k = k + 1
                print("review number: ",k)
                print("i: ", i)
                print("j:", j)
               
                
            print(username)
            rating_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k) +"]/div/div[2]/div[1]/div[1]/div/span[1]/div/div") 
            rating = driver.find_element_by_xpath(rating_pth).get_attribute("aria-label")
            date_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k) +"]/div/div[2]/div[1]/div[1]/div/span[2]")
            date = driver.find_element_by_xpath(date_pth).text
            
            #Click Full Review if icon exists
            try: 
                fullRev_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div["+ str(k) +"]/div/div[2]/div[2]/span[1]/div/button")
                fullRev = driver.find_element_by_xpath(fullRev_pth)
            except NoSuchElementException as exception: 
                print("Short Review.")
                review_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k) +"]/div/div[2]/div[2]/span[1]")
                review = driver.find_element_by_xpath(review_pth).text
            else:
                print("Long review")
                fullRev.click()
                time.sleep(2)
                review_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k) +"]/div/div[2]/div[2]/span[2]")
                review = driver.find_element_by_xpath(review_pth).text
                               
            with open('Iteration 3/scrapedData/debug/'+appname+'_username.csv',"a") as output_file:
                json.dump({"username": username},output_file)
            with open('Iteration 3/scrapedData/debug/'+appname+'_rating.csv',"a") as output_file:
                json.dump({"dump_rating": rating},output_file)
            with open('Iteration 3/scrapedData/debug/'+appname+'_date.csv',"a") as output_file:
                json.dump({"date": date},output_file)
            with open('Iteration 3/scrapedData/debug/'+appname+'_review.csv',"a") as output_file:
                json.dump({"text": review},output_file)
            #tmp = []
            # tmp.append({"app_name":appname,
            # "username":username,
            # "rating":rating,
            # "review":review,
            # "date":date})
            
            tmp = [appname, username, rating, review, date]
    
            with open('Iteration 3/'+appname+'.csv',"a") as output_file:
                fieldnames = ['app_name', 'username', 'rating','review', 'date']
                #output_file.write(str(tmp) + '\n')
                writer = csv.DictWriter(output_file, delimiter=',',fieldnames=fieldnames)
                writer.writerow({'app_name':appname,'username':username,'rating':rating,'review':review, 'date':date})
            with open('Iteration 3/'+appname+'.json',"a") as output_file:
                json.dump(tmp,output_file)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    try:
        element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div").click();
    except NoSuchElementException as exception: 
        print("'Show More' not found. Continuing to scroll.")
        continue
