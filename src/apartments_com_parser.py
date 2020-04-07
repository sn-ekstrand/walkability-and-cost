from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['apartments_com']
table = db['austin_apartments']

# Import BeautifulSoup
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
from pymongo import MongoClient
import pprint



# borrowed and adapted code from Chuanxiu Xiong
# https://github.com/chuanxiuXiong/apartments.com-scraper/blob/master/scraper.py
request_header = {
#         'Accept': "application/json, text/javascript, */*; q=0.01",
#         'Accept-Encoding': "gzip, deflate, br",
#         'Accept-Language': "en-US, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3",
#         'Cache-Control': "no-cache",
#         'Content-Type': "application/json",
#         'Host': "www.apartments.com",
#         'Origin': "https://www.apartments.com",
#         'Referer': "https://www.apartments.com/",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
#         'X-Requested-With': "XMLHttpRequest",
        }

## Iterate through all pages for a city
for page in range(28):
    base_url = "https://www.apartments.com/austin-tx/{}/".format(page+1)
    r = requests.get(base_url, headers=request_header)
    page_status = r.status_code

# save to mongodb?


    soup = BeautifulSoup(r.text, 'html.parser')

    # grab just the html for the specific apartments on the page
    placards = soup.find_all('article', 'diamond placard')

    # grab the html text for each apartment on a page
    for apt in len(placards):
        tag = placards[apt]
        link = tag['data-url'] 
        sub_page = requests.get(link, headers=request_header)
        sub_soup = BeautifulSoup(sub_page.text, 'html.parser')

        # append html to MongoDB