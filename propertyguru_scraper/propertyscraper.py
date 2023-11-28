import cloudscraper
import time
import re
import os
import pandas as pd
import numpy as np
import pickle
from datetime import datetime
from bs4 import BeautifulSoup
from geopy.geocoders import GoogleV3

# set parameters
url = 'https://www.propertyguru.com.my/property-for-sale?freetext=Kuala+Lumpur&property_type=N&property_type_code%5B0%5D=APT&property_type_code%5B1%5D=CONDO&property_type_code%5B2%5D=DUPLX&property_type_code%5B3%5D=FLAT&property_type_code%5B4%5D=PENT&property_type_code%5B5%5D=SRES&property_type_code%5B6%5D=STDIO&property_type_code%5B7%5D=TOWNC&region_code=MY14&search=true'
start_scrap_page = 1
geolocator = GoogleV3(api_key='') #Insert your Google Map API key for geocoding
scraper = cloudscraper.create_scraper(delay=10)

def get_pagination(url):
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pagination = soup.find('ul', class_='pagination')
    pages = pagination.find_all('a')
    lastPage = int(pages[-2]['data-page'])
    return lastPage

def scrape_listing(startPage, endPage):
    counter = 0
    area_list = listing_areas()
    
    for page in range(startPage, endPage + 1):
        time.sleep(random.randint(5,10))
        url = 'https://www.propertyguru.com.my/property-for-sale/'+str(page)+'?freetext=Kuala+Lumpur&property_type=N&property_type_code%5B0%5D=APT&property_type_code%5B1%5D=CONDO&property_type_code%5B2%5D=DUPLX&property_type_code%5B3%5D=FLAT&property_type_code%5B4%5D=PENT&property_type_code%5B5%5D=SRES&property_type_code%5B6%5D=STDIO&property_type_code%5B7%5D=TOWNC&region_code=MY14&search=true'
        scraper = cloudscraper.create_scraper(delay=10)
        response = scraper.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        listing_results = soup.find_all(attrs={'class':'listing-card-sale', 'itemtype':'https://schema.org/Place', 'data-unit-type-id': None})
    
        for items in listing_results:
            try:
            
                if items['data-listing-id'] in scraped_listing_ids:
                    print(f"Listing {items['data-listing-id']} has already been scraped")
                    continue
            
                listingId = items['data-listing-id']
                title = items.find('a', class_='nav-link').string
                location = items.find('span', itemprop='streetAddress').string
                price = items.find('span', class_='price').string.replace(',',"")
                bed = items.find('span', class_='bed').get_text()
                bath = items.find('span', class_='bath').get_text()
                sqft = items.find('li', class_='listing-floorarea pull-left').get_text().split()[0]
                psf = items.find(string=re.compile('psf')).split()[1]
                listingURL = items.find('a', class_='nav-link')['href']
                propType = items.find('ul', class_='listing-property-type').get_text().strip().split("\n")
                
                completionYear = np.nan
                titleType = np.nan
                buildingType = np.nan
                
                for item in propType:
                    if 'Completion:' in item:
                      completionYear = ''.join(re.findall(r'\d+', item))
                    if 'Freehold' in item or 'Leasehold' in item:
                      titleType = item
                    if 'Completion:' not in item and ('Freehold' not in item and 'Leasehold' not in item):
                      buildingType = item
                
                if location:
                    for area in area_list:
                      if re.search(area, location):
                        break
                
                scraped_listing_ids.add(listingId)
            
            except Exception as e:
              print(f"Error in scraping {listingId}: {title} due to {e}")
            
            else:
            
              data_list.append({
                    "id": listingId,
                    "title": title,
                    "location": location,
                    "price": price,
                    "bed": bed,
                    "bath": bath,
                    "sqft": sqft,
                    "psf": psf,
                    "year": completionYear,
                    "titleType": titleType,
                    "buildingType": buildingType,
                    "url": listingURL,
                    "address": title + ', ' + location,
                    "area": area})
            
              counter += 1
        if "captcha" in soup.text:
            print(f"Page {page} blocked by captcha, skipped.")
        else:
            print(f'Successfully scraped page {page} of {endPage}. Total {counter} listing scraped.')
    
    return pd.DataFrame(data_list)

def listing_areas():
  url = 'https://www.propertyguru.com.my/kuala-lumpur'
  response = scraper.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  state_areas = soup.find_all('div', class_='list-group-item list-group-item-single')
  area_list = set()

  for i in state_areas:
    get_areas = i.find_all('li', class_='col-xs-6 col-sm-3')

    for location in get_areas:
      area = location.get_text()
      area_list.add(area)
  return area_list

def geocoder(df, geolocator):
  try:
    with open('geocoded_addresses.pkl', 'rb') as addresses_file:
        geocoded_addresses = pickle.load(addresses_file)
  except FileNotFoundError:
      geocoded_addresses = pd.DataFrame(columns=['unique_titles', 'full_address', 'latitude', 'longitude'])

  geodf = pd.DataFrame(columns=['unique_titles', 'full_address', 'latitude', 'longitude'])
  
  for i in df['address'].unique():
    if i in geocoded_addresses['unique_titles'].unique():
      print(f"Did not geocode {i}")
      continue
    
    location = geolocator.geocode(i)
    if location:
      new_data = pd.DataFrame({'unique_titles': [i], 'full_address': [location.address], 'latitude': [location.latitude], 'longitude': [location.longitude]})
      geodf = pd.concat([geodf, new_data], ignore_index=True)
      print(f"Geocoded - {i}")

  geocoded_addresses = pd.concat([geocoded_addresses, geodf], ignore_index=True)
  print("Geocoded address list updated")

  with open('geocoded_addresses.pkl', 'wb') as addresses_file:
      pickle.dump(geocoded_addresses, addresses_file)

  propertyloc = pd.merge(df, geocoded_addresses, left_on='address', right_on='unique_titles', how='left')
  propertyloc.drop(['address', 'unique_titles'], axis=1, inplace=True)
  return propertyloc

def main():
  scrap_df = scrape_listing(start_scrap_page, get_pagination(url))
  property_df = geocoder(scrap_df, geolocator)
  currentDateTime = datetime.now().strftime("%m-%d-%Y %H-%M-%S %p")
  property_df.to_csv(f"../data/properties_raw_{currentDateTime}.csv", index = False)
  return property_df

if __name__ == "__main__":
  scraped_listing_ids = set()
  data_list = []
  df = main()
  df