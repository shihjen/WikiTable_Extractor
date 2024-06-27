# import essential libraries
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json

# Streamlit page configuration
st.set_page_config(page_title='WikiTable Extractor',
                   page_icon = ':wrench:',
                   layout = 'wide',
                   initial_sidebar_state = 'auto')

# function to load the lottie file
def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)
lottie_cover = load_lottiefile('img/cover.json')    

# function to convert the extracted table in csv format
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

# application description
description = '''
The WikiTable Extractor is designed to simplify the process of extracting tables from Wikipedia pages. 
By entering the URL of a Wikipedia page, users can quickly and efficiently pull all the tables present on the page into a usable format. 
This tool leverages the extensive data resources available on Wikipedia, making it a valuable asset for anyone needing to analyze, manipulate, or repurpose structured data.
'''



col1, col2 = st.columns([1,3],gap='large')

with col1:
    st.title('WikiTable Extractor')
    st.write(f'##### {description}')
    st.lottie(lottie_cover, speed=1, reverse=False, loop=True, quality='low', height=500, key='first_animate')
    container = st.container(border=True)
    container.title('URL Input')

    url = container.text_input('Paste the URL Link')

    if url:
        try:
            html = requests.get(url).content
            df_list = pd.read_html(html)

            number_table = len(df_list)

            container.write(f'Total {number_table} table(s) found in the webpage {url}.')

            with col2:
                if number_table > 0:
                    for i in range(number_table):
                        st.markdown(f'### Table {i+1}')
                        st.dataframe(df_list[i], use_container_width=True)
                        csv = convert_df(df_list[i])
                        st.download_button(
                            label='Download data as CSV',
                            data=csv,
                            file_name=f'table{i+1}.csv',
                            mime='text/csv',
                            )
        except:
            st.write('Invalid Input')


