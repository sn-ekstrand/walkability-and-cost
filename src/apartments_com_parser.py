import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
from pymongo import MongoClient
import pprint

client = MongoClient('localhost', 27017)
db = client['apartments_com']
city_pages_table = db['city_pages']
ind_apts_table = db['individual_apartments']


# borrowed and adapted code from Chuanxiu Xiong
# https://github.com/chuanxiuXiong/apartments.com-scraper/blob/master/scraper.py
request_header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    }

# cities = ['austin-tx', 'new-york-ny', 'san-francisco-ca', 'boston-ma', 'seattle-wa', 'portland-or', 'phoenix-az', 'el-paso-tx', 'oklahoma-city-ok', 'indianapolis-in']

cities = ['austin-tx', 'san-francisco-ca', 'indianapolis-in']

for city in cities:
    # Iterate through all pages for a city
    # The max number of pages appears to always be 28
    for page in range(28):
        base_url = "https://www.apartments.com/{}/{}/".format(city, page+1)
        r = requests.get(base_url, headers=request_header)
        time.sleep(np.random.randint(18, 33))

        # save to mongodb
        city_pages_table.insert_one({'city': city, 'page_number': (page+1), 'url': base_url, 'html': r.text})

        # grab just the html for the specific apartments on the page
        soup = BeautifulSoup(r.text, 'html.parser')
        placards = soup.find_all('article', 'placard')
        for idx, apt in enumerate(placards):
            tag = placards[idx]
            sub_page_url = tag['data-url'] 
            listing_id = tag['data-listingid']
            sub_page_html = requests.get(sub_page_url, headers=request_header)
            time.sleep(np.random.randint(18, 33))

            # append sub page html to MongoDB
            ind_apts_table.insert_one({'city': city, 'listing_id': listing_id, 'url': sub_page_url, 'html': sub_page_html.text})

