import streamlit as st  
import pandas as pd    
 
from visualization import visualization
from visualization import page_4
from data_manag import data_man
from Introduction import intro
from Analysis import analysis

st.set_page_config(layout="wide")

data = pd.read_csv('data/data_manag_final_v.csv')
im = "data/image.png"
txt = "data/contenu_clean.txt"
page = st.sidebar.radio("projet-sda-dash-streamlit", ["Introduction", "Data Management", "Analysis", "Data Visualization", "WordCloud"])

if page == "Introduction":
    intro()
elif page == "Data Management":
    data_man()
elif page == "Data Visualization":
    visualization(data)
elif page == "Analysis":
    analysis(data)
elif page == "WordCloud":
    page_4(txt,im)

