import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json

st.set_page_config(page_title='Wikipedia Table Extractor',
                   page_icon = ':wrench:',
                   layout = 'wide',
                   initial_sidebar_state = 'auto')

# function to load the lottie file
def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)
lottie_cover = load_lottiefile('img/cover.json')    

st.title('Wikipedia Table Extractor')
col1, col2 = st.columns([1,3],gap='large')

with col1:
    st.lottie(lottie_cover, speed=1, reverse=False, loop=True, quality='low', height=500, key='first_animate')
    container = st.container(border=True)
    container.title('URL Input')

    url = container.text_input('Paste the URL Link')

    if url:
        html = requests.get(url).content
        df_list = pd.read_html(html)

        number_table = len(df_list)

        container.write(f'Total {number_table} table(s) found in the webpage {url}.')

        with col2:
            if number_table > 0:
                for i in range(number_table):
                    st.markdown(f'### Table {i+1}')
                    st.dataframe(df_list[i], use_container_width=True)


