# PropertyGuru-Scraper
This is a scraper that I built to extract residential apartment and condos properties for sale in Kuala Lumpur.

There are two parts to the project:
1. Web scraper
2. Dashboard

The goal is to identify undervalued properties on sale.

This project is done for educational purposes only.

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

There are two main sections to the dashboard:
1) Analytics and/or general summary of the scraped listings
2) A map plotted with all the scraped listings

