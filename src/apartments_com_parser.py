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


# custom header for the scraper to function longer before being stopped
request_header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    }

def scrape_city(city_tag):        
    # Iterate through all pages for a city
    # The max number of pages appears to always be 28
    for page in range(1, 28+1):
        base_url = "https://www.apartments.com/city_tag/{}/".format(page)
        r = requests.get(base_url, headers=request_header)
        time.sleep(np.random.randint(25, 40))

        # save to mongodb
        city_pages_table.insert_one({'city': city_tag, 'page_number': (page), 'url': base_url, 'html': r.text})

        # grab just the html for the specific apartments on the page
        soup = BeautifulSoup(r.text, 'html.parser')
        placards = soup.find_all('article', 'placard')
        for idx, apartment in enumerate(placards):
            tag = placards[idx]
            sub_page_url = tag['data-url'] 
            listing_id = tag['data-listingid']
            sub_page_html = requests.get(sub_page_url, headers=request_header)
            time.sleep(np.random.randint(25, 40))

            # append sub page html to MongoDB
            ind_apts_table.insert_one({'city': 'seattle-wa', 'listing_id': listing_id, 'url': sub_page_url, 'html': sub_page_html.text})

        time.sleep(np.random.randint(50, 70))


# cities = ['austin-tx', 'new-york-ny', 'san-francisco-ca', 'boston-ma', 'seattle-wa', 'portland-or', 'phoenix-az', 'el-paso-tx', 'oklahoma-city-ok', 'indianapolis-in']
city_tags = ['austin-tx', 'san-francisco-ca', 'indianapolis-in']

for city in cities:
    scrape_city(city)