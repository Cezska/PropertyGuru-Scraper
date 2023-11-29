# PropertyGuru Scraper
This is a scraper that I built to extract residential apartment and condos properties for sale in Kuala Lumpur.

There are two parts to the project:
1. Web scraper
2. Dashboard

The goal is to identify undervalued properties on sale. The scraper by default is scraping only apartment, condo and serviced residence as these properties are easier to compare apple-to-apple as compared to landed properties and has higher volume.

This project is done for educational purposes only.

NOTE: The web scraper is currently being blocked by captcha from the site and therefore is only able to scrape a limited amount of listings. To bypass this, it's recommended to incorporate paid captcha solvers into the get requests.

## Repository overview
```
📦 
├─ .gitignore
├─ .streamlit
│  └─ config.toml
├─ LICENSE
├─ README.md
├─ data
│  └─ properties_raw_11-27-2023 23-16-29 PM.csv
├─ propertyguru_scraper
│  ├─ __init__.py
│  ├─ geocoded_addresses.pkl
│  ├─ propertyscraper.py
│  └─ requirements.txt
└─ streamlit_dashboard
   ├─ __init__.py
   ├─ requirements.txt
   └─ streamlit_app.py
```

## Installation
The scraper was built using BeautifulSoup4. 
The dashboard was built using Streamlit.

To use, make sure to have all the dependencies installed. 

You may download the [requirements.txt (for scraper)](https://github.com/Cezska/PropertyGuru-Scraper/blob/669f76bff3a5cdeeaddefbd11fa2bac2ed1b5274/propertyguru_scraper/requirements.txt) or [requirements.txt (for dashboard)](https://github.com/Cezska/PropertyGuru-Scraper/blob/669f76bff3a5cdeeaddefbd11fa2bac2ed1b5274/propertyguru_scraper/requirements.txt](https://github.com/Cezska/PropertyGuru-Scraper/blob/669f76bff3a5cdeeaddefbd11fa2bac2ed1b5274/streamlit_dashboard/requirements.txt)https://github.com/Cezska/PropertyGuru-Scraper/blob/669f76bff3a5cdeeaddefbd11fa2bac2ed1b5274/streamlit_dashboard/requirements.txt) and run the following

Pip:

```pip install -r requirements.txt```

Conda:

```conda install --file requirements.txt```

## Web scraper
The scraper by default is fitted with a URL from PropertyGuru. The URL has existing filter for `Apartment/Condo/Serviced Residence` and `Kuala Lumpur` listings. Therefore, only listings that meets the two criterias would be scraped.

Output will be saved in a CSV under `data` folder.

### Output data from scraper
| Column       | Description                                                                |
|--------------|----------------------------------------------------------------------------|
| id           | Listing ID                                                                 |
| title        | Listing title                                                              |
| location     | Location of property from listing                                          |
| price        | Price of property                                                          |
| bed          | No of bedrooms                                                             |
| bath         | No of bathrooms                                                            |
| sqft         | Total sqft of property                                                     |
| psf          | Price per sqft of property                                                 |
| year         | Property year built (0 if data not available)                              |
| titleType    | Title type of property                                                     |
| buildingType | Building type of property                                                  |
| url          | Link to property listing                                                   |
| area         | Location area of property from listing                                     |
| full_address | Address of property from Google Maps based on title and listing location   |
| latitude     | Latitude of property from Google Maps based on title and listing location  |
| longitude    | Longitude of property from Google Maps based on title and listing location |

`full_address`, `latitude` and `longitude` columns are data obtained through geocoding of the title+location of the listing. Geocoding is done via Google Maps.

### Usage
Do fill in the parameters at the top of the script as your need.
Do ensure the URLs on three sections are updated accordingly.
1. Parameters section (first page/beginning page of the listing directory to scrape from)
2. scrape_listing function (has to match #1)
3. listing_areas function (only change this to match the area in #1 & #2 if you're scraping area other than Kuala Lumpur otherwise may leave as is)

## Dashboard
The dashboard is built and hosted on Streamlit [here](https://propertyguru-scraper-project.streamlit.app/).

<img src="https://github.com/Cezska/cezska.github.io/assets/102790793/6a87abcf-25de-4cfe-9a3b-e36bdd23e16c?raw=true" width="1000"/>


There are two main sections to the dashboard:
1) Analytics and/or general summary of the scraped listings
2) A map plotted with all the scraped listings

There is a map filters on the left of the dashboard. This filter will only update the results on the map as well as the tables beneath the map.

As the purpose of this is to identify _undervalued_ properties for sale, the map and tables beneath the map is done with that in mind.

On the map, pins are colored:
1. Green indicates that there is one or more listing for sale at a price below the median price of the property or median price of the property area
2. Red indicates that there is no listing for sale at a price below the median price of the property or median price of the property area


<table class="tg">
<thead>
  <tr>
    <th class="tg-0pky">Column</th>
    <th class="tg-0pky">Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0pky">id</td>
    <td class="tg-0pky">Listing ID</td>
  </tr>
  <tr>
    <td class="tg-0pky">title</td>
    <td class="tg-0pky">Listing title</td>
  </tr>
  <tr>
    <td class="tg-0pky">location</td>
    <td class="tg-0pky">Location of property from listing</td>
  </tr>
  <tr>
    <td class="tg-0pky">price</td>
    <td class="tg-0pky">Price of property</td>
  </tr>
  <tr>
    <td class="tg-0pky">bed</td>
    <td class="tg-0pky">No of bedrooms</td>
  </tr>
  <tr>
    <td class="tg-0pky">bath</td>
    <td class="tg-0pky">No of bathrooms</td>
  </tr>
  <tr>
    <td class="tg-0pky">sqft</td>
    <td class="tg-0pky">Total sqft of property</td>
  </tr>
  <tr>
    <td class="tg-0pky">psf</td>
    <td class="tg-0pky">Price per sqft of property</td>
  </tr>
  <tr>
    <td class="tg-0pky">year</td>
    <td class="tg-0pky">Property year built (0 if data not available)</td>
  </tr>
  <tr>
    <td class="tg-0pky">titleType</td>
    <td class="tg-0pky">Title type of property</td>
  </tr>
  <tr>
    <td class="tg-0pky">buildingType</td>
    <td class="tg-0pky">Building type of property</td>
  </tr>
  <tr>
    <td class="tg-0pky">url</td>
    <td class="tg-0pky">Link to property listing</td>
  </tr>
  <tr>
    <td class="tg-0pky">area</td>
    <td class="tg-0pky">Location area of property from listing</td>
  </tr>
  <tr>
    <td class="tg-0pky">full_address</td>
    <td class="tg-0pky">Address of property from Google Maps based on title and listing location</td>
  </tr>
  <tr>
    <td class="tg-0pky">latitude</td>
    <td class="tg-0pky">Latitude of property from Google Maps based on title and listing location</td>
  </tr>
  <tr>
    <td class="tg-0pky">longitude</td>
    <td class="tg-0pky">Longitude of property from Google Maps based on title and listing location</td>
  </tr>
</tbody>
</table>
