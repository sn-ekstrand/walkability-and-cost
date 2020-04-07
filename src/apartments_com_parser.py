from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['apartments_com']
austin_apts_table = db['austin_apartments']
apts_pages_table = db['apartment_pages']

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
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    }

# Iterate through all pages for a city
# The max number of pages appears to always be 28
for page in range(28):
    base_url = "https://www.apartments.com/austin-tx/{}/".format(page+1)
    r = requests.get(base_url, headers=request_header)
    
    # save to mongodb
    austin_apts_table.insert_one({'page_number': page, 'url': base_url, 'html': r.text})

    time.sleep(10)

    # grab just the html for the specific apartments on the page
    soup = BeautifulSoup(r.text, 'html.parser')
    placards = soup.find_all('article', 'placard')
    for apt in len(placards):
        tag = placards[apt]
        sub_page_url = tag['data-url'] 
        listing_id = tag['data-listingid']
        sub_page_html = requests.get(sub_page_url, headers=request_header)

        # append sub page html to MongoDB
        apts_pages_table.insert_one({'listing_id': listing_id, 'url': sub_page_url, 'html': sub_page_html.text})

        time.sleep(10)

