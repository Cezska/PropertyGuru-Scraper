import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
import plotly.express as px 

datafile = pd.read_csv("data/properties_raw_11-27-2023 23-16-29 PM.csv")
datafile['psf'] = datafile['psf'].replace(',', '', regex=True).astype(float).round(0)
datafile['year'] = datafile['year'].fillna(0).astype(int)

area_median = datafile.groupby('area')['psf'].median()
listing_count = datafile['title'].value_counts().to_dict()

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Filters section #
st.sidebar.header('Map filters')
st.sidebar.write('')
listing_areas = sorted(datafile['area'].unique())
listing_areas.insert(0, 'Show All Areas')

selected_area = st.sidebar.selectbox('Select area', listing_areas, placeholder='Choose an option')
st.sidebar.write('')

if selected_area == 'Show All Areas':
  filtered_data = datafile.sort_values(by=['title', 'psf'], ascending=True)
else:
  filtered_data = datafile[datafile['area'] == selected_area].sort_values(by=['title', 'psf'], ascending=True)

price_slider = st.sidebar.slider('Property price', filtered_data['price'].min(), filtered_data['price'].max(), (filtered_data['price'].min(), filtered_data['price'].max()))

sqft_slider = st.sidebar.slider('Property sqft', filtered_data['sqft'].min(), filtered_data['sqft'].max(), (filtered_data['sqft'].min(), filtered_data['sqft'].max()))

title_selector = st.sidebar.multiselect('Title type', filtered_data['titleType'].unique(), default=filtered_data['titleType'].unique())
building_selector = st.sidebar.multiselect('Building type', filtered_data['buildingType'].unique(), default=filtered_data['buildingType'].unique())

if price_slider:
    filtered_data = filtered_data[(filtered_data['price'] >= price_slider[0]) & (filtered_data['price'] <= price_slider[1])] 
if sqft_slider:
    filtered_data = filtered_data[(filtered_data['sqft'] >= sqft_slider[0]) & (filtered_data['sqft'] <= sqft_slider[1])]
if title_selector:
    filtered_data = filtered_data[filtered_data['titleType'].isin(title_selector)]
if building_selector:
    filtered_data = filtered_data[filtered_data['buildingType'].isin(building_selector)]

st.sidebar.markdown('***')
st.sidebar.write(f'Total **{filtered_data.shape[0]}** listings found')
###########################

st.title("Properties for sale in Kuala Lumpur")

tab1, tab2 = st.tabs(['Charts', 'Table'])

area_grouped = datafile.groupby('area')
area_agg = pd.DataFrame()
area_agg['total_listings'] = area_grouped['title'].count()
area_agg[['min_price','max_price','median_price']] = area_grouped['price'].agg(['min','max','median'])
area_agg['median_psf'] = area_grouped['psf'].median()
area_agg['median_sqft'] = area_grouped['sqft'].median().astype('int')
area_agg = area_agg.reset_index()

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:

        col1.subheader('Total listings by areas')
        area_listings=px.bar(area_agg.sort_values(by='area', ascending=False),x='total_listings',y='area', orientation='h', text='total_listings')
        area_listings.update_traces(textposition = 'outside')
        col1.plotly_chart(area_listings, use_container_width=True)
    
    with col2:
        
        col2.subheader('Breakdown by building type')
        buildingType_grouped = datafile.groupby('buildingType')
        buildingType_agg = pd.DataFrame()
        buildingType_agg['total_listings'] = buildingType_grouped['title'].count()
        buildingType_agg = buildingType_agg.reset_index()
        donut_chart = px.pie(buildingType_agg.sort_values(by='buildingType', ascending=False), values='total_listings', names='buildingType')
        col2.plotly_chart(donut_chart, use_container_width=True)

    st.subheader('Median price by areas')
    area_med_price=px.bar(area_agg.sort_values(by='area', ascending=False),x='median_price',y='area', orientation='h', text='median_price')
    area_med_price.update_traces(texttemplate='RM%{text:,}', textposition = 'outside')
    st.plotly_chart(area_med_price, use_container_width=True)

    st.subheader('Median PSF by areas')
    area_med_psf=px.bar(area_agg.sort_values(by='area', ascending=False),x='median_psf',y='area', orientation='h', text='median_psf')
    area_med_psf.update_traces(texttemplate='RM%{text:,}', textposition = 'outside')
    st.plotly_chart(area_med_psf, use_container_width=True)

    st.subheader('Sqft vs property price, by areas')
    st.write('Bubble size is _number of total listings in the area_')
    st.scatter_chart(
        area_agg,
        x='median_price',
        y='median_sqft',
        color='area',
        size='total_listings',
        use_container_width = True)
    
    st.subheader('Properties by year built')
    st.write('Excludes properties without year data')
    year_data = datafile[datafile['year'] != 0].groupby('year')['id'].count().reset_index(name='total_listings')
    year_breakdown=px.bar(year_data.sort_values(by='year', ascending=False),x='year',y='total_listings', text='total_listings')
    st.plotly_chart(year_breakdown, use_container_width=True)

    

with tab2:
    st.subheader('Area summary')
    st.dataframe(area_agg,
                 height=int((len(area_agg.reset_index(drop=True))+1) * 35),
                 column_config = {
                     'min_price': st.column_config.NumberColumn(help = 'Minimum price of property listing in RM'),
                     'max_price': st.column_config.NumberColumn(help = 'Maximum price of property listing in RM'),
                     'median_price': st.column_config.NumberColumn(help = 'Median price of property listing in RM'),
                     'median_sqft': st.column_config.NumberColumn(help = 'Median property sqft of listings in RM')},
                 use_container_width = True,
                 hide_index = True)

# In the section below we build the map #
st.markdown("***")
st.title("Location of properties for sale")
st.write("Pin colors indicate potential undervalued properties based on building's and/or area's median price")

try:
    map_center = (filtered_data['latitude'].mean(), filtered_data['longitude'].mean())
    map = folium.Map(map_center, tiles='cartodbpositron', zoom_start=12)
    
    for i, row in filtered_data.iterrows():
        undervalued_by_area = filtered_data[filtered_data['psf'] < area_median.loc[row['area']]]['title'].value_counts().to_dict().get(row['title'],0)
        undervalued_by_area_buildings = filtered_data[(filtered_data['psf'] < area_median.loc[row['area']]) & (filtered_data['psf'] < row['psf'])]['title'].value_counts().to_dict().get(row['title'],0)
        iframe = folium.IFrame(
                                f"{row['title']}<br><br>"
                                f"Area: {row['area']}<br>"
                                f"Area median PSF: RM{area_median.loc[row['area']]:,.0f}<br>"
                                f"Building median PSF: RM{row['psf']:,.0f}<br>"
                                f"Total available listings: {listing_count.get(row['title'])}<br><br>"
                                f"No of listings with psf below area median psf: {undervalued_by_area}<br>"
                                f"No of listings with psf below area & building median psf: {undervalued_by_area_buildings}<br>"
                            )
        popup = folium.Popup(iframe, min_width=400, max_width=400)
        color = ('darkgreen' if undervalued_by_area+undervalued_by_area > 0 else 'crimson')
        location = (row['latitude'], row['longitude'])
        marker = folium.Marker(
                                location,
                                radius = (row['psf']/area_median.loc[row['area']])*10,
                                fill = True,
                                icon = folium.Icon(color=color,icon='home', prefix='fa'),
                                fill_opacity = 1,
                                popup = popup)
        marker.add_to(map)
    st_folium(map, width = 1500)
    
except Exception:
    map = folium.Map((3.147740871242468, 101.69837799154377), tiles='cartodbpositron', zoom_start=12)
    st_folium(map, width = 1500)
    pass
    
if len(filtered_data) != 0:
    min_value = int(filtered_data['sqft'].min()),
    max_value = int(filtered_data['sqft'].max())
else:
    min_value = 0
    max_value = 0

st.write("List of property listings found based on filters:")
st.dataframe(filtered_data, 
             column_order = ('area', 'title', 'price', 'sqft', 'psf', 'bed', 'bath', 'year', 'titleType', 'buildingType', 'full_address', 'url'),
             column_config = {
                 'title': st.column_config.TextColumn(width='medium'),
                 'psf': st.column_config.ProgressColumn(
                    format = "RM%f",
                    min_value = min_value,
                    max_value = max_value),
                 'year': st.column_config.TextColumn(),
                 'full_address': st.column_config.TextColumn(width='medium'),
                 'url': st.column_config.LinkColumn('URL')},
             hide_index = True)

st.write("List of undervalued property listings found based on filters:")
st.dataframe(filtered_data[filtered_data['area'].map(area_median) > filtered_data['psf']], 
             column_order = ('area', 'title', 'price', 'sqft', 'psf', 'bed', 'bath', 'year', 'titleType', 'buildingType', 'full_address', 'url'),
             column_config = {
                 'title': st.column_config.TextColumn(width='medium'),
                 'psf': st.column_config.ProgressColumn(
                    format = "RM%f",
                    min_value = min_value,
                    max_value = max_value),
                 'year': st.column_config.TextColumn(),
                 'full_address': st.column_config.TextColumn(width='medium'),
                 'url': st.column_config.LinkColumn('URL')},
             hide_index = True)
