import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
from bs4 import BeautifulSoup

st.title('World Athletics Records Explorer')

st.markdown("""
This app performs simple webscraping of World Athletics records data!
* **Python libraries:** base64, pandas, streamlit, requests, beautifulsoup4
* **Data source:** [Worldathletics.org](https://worldathletics.org/records/all-time-toplists/sprints/100-metres/outdoor/men/senior).
""")

st.sidebar.header('User Input Features')
selected_event = st.sidebar.selectbox('Event', ['100 metres', '200 metres', '400 metres'])
selected_gender = st.sidebar.selectbox('Gender', ['Men', 'Women'])

# Web scraping of World Athletics records
@st.cache
def load_data(event, gender):
    url = f'https://worldathletics.org/records/all-time-toplists/sprints/{event.lower().replace(" ","-")}/outdoor/{gender.lower()}/senior'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    headers = [header.text.strip() for header in table.find_all('th')]
    data = []
    for row in table.find_all('tr')[1:]:
        data.append([cell.text.strip() for cell in row.find_all('td')])
    df = pd.DataFrame(data, columns=headers)
    return df
record_stats = load_data(selected_event, selected_gender)

# Sidebar - Country selection
sorted_unique_country = sorted(record_stats.Country.unique())
selected_country = st.sidebar.multiselect('Country', sorted_unique_country, sorted_unique_country)

# Sidebar - Discipline selection
unique_discipline = ['100m', '200m', '400m']
selected_discipline = st.sidebar.multiselect('Discipline', unique_discipline, unique_discipline)

# Filtering data
df_selected_country = record_stats[(record_stats.Country.isin(selected_country)) & (record_stats.Discipline.isin(selected_discipline))]

st.header('Display Record Stats of Selected Country(s) and Discipline(s)')
st.write('Data Dimension: ' + str(df_selected_country.shape[0]) + ' rows and ' + str(df_selected_country.shape[1]) + ' columns.')
st.dataframe(df_selected_country)

# Download World Athletics records data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="recordstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_country), unsafe_allow_html=True)