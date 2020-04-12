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
    for city in city_tag_list:
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

scrape_city(city_tags)

#create blank dataframe with just column names
df_columns = ['listing_id', 'property_name', 'address', 'mean_rent', 'mean_area', 'walkscore']
df = pd.DataFrame(columns=df_columns)

apartment_collection = ind_apts_table.find()
 
# populate dataframe
for apartment in ind_apts_table.find():
    soup = BeautifulSoup(apartment['html'], 'html.parser')
    
    listing_id = apartment['listing_id']
    property_name = soup.find('h1', 'propertyName').text.strip()
    address_ = soup.find('div', 'propertyAddress').find('h2').text
    address = ' '.join(address_.split())
    
    # iterate through each unit and find mean price and area
    max_rents = []
    unit_areas = []
    for unit in soup.find('table', 'availabilityTable').find('tbody').find_all('tr', 'rentalGridRow'):
        availability = unit.find('td', 'available').text.strip()
        # only look at max rents for simplicity
        unit_max_rent = unit['data-maxrent']
        if (availability == 'Available Now') and (unit_max_rent != ''):
            max_rents.append(int(unit_max_rent))
        else:
            break
        unit_area_str = unit.find('td', 'sqft').text.strip(' Sq Ft')
        unit_area_range = unit_area_str.replace(',', '').split(' - ')
        try:
            unit_area_range = [int(area) for area in unit_area_range]
            unit_area = (max(unit_area_range) + min(unit_area_range) / 2)
            unit_areas.append(unit_area)
        except:
            print('unit_area problem: {}'.format(address))
            
    mean_rent = 0
    mean_area = 0
    try:
        mean_rent = sum(max_rents) / len(max_rents)
        mean_area = sum(unit_areas) / len(unit_areas)
    except:
        print('problem: {}'.format(address))
    
    walkscore = int(soup.find('div', 'ratingCol walkScore').find('span', 'score').text)
    
    #add info to DF
    row = pd.DataFrame([[listing_id, 
                         property_name, 
                         address, 
                         mean_rent, 
                         mean_area, 
                         walkscore]], columns=df_columns)
    df = df.append(row, ignore_index=True)
    
    
# drop apartments without rent listed
df = df[df['mean_rent'] != 0]

df['cost/SF'] = (df['mean_rent'] / df['mean_area'])
df.sort_values(by='cost/SF')

#export to csv
df.to_csv('../data/apartments_dataframe.csv', index=False)