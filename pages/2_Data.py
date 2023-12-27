import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import os
import sys

st.set_page_config(page_title = "Data Info", page_icon = '📊', layout='wide')
sys.path.insert(0, '/MPG_PRED')
def hide_footer():
  hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
  st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_footer()


st.markdown("# Fuel Efficiency Dataset")

st.sidebar.header("Dataset info")

st.write(
    """This page shows the dataset that was used for this application."""
)

current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.split(current_path)[0]
data_file = os.path.join(parent_path, "data/auto-mpg.csv")

@st.experimental_memo
#@st.cache_data
def get_base_data():
  file = '.././data/auto-mpg.csv'
  base_data = pd.read_csv(data_file)
  return base_data

@st.experimental_memo
#@st.cache_data
def get_transform_data(df):
  df_data = df.copy()
  df_data.displacement = df_data.displacement.astype(np.int64)
  car_names = df_data['car name']
  df_data['car_type'] = [1 if 'diesel' in i else 0 for i in car_names]
  df_data = df_data.drop(['car name'], axis=1)
  df_data.reset_index()
  return df_data

try:
  mpg_data = get_transform_data(get_base_data())
  with st.expander("Car Info Dataset", expanded=True):
    c1, c2 = st.columns((2, 3))
    with c1:
      st.header("Dataframe")
      st.dataframe(data=mpg_data)
    with c2:
      st.header("Descriptive Info of dataset")
      st.write(mpg_data.describe())
except Exception as e:
  st.write('An error has occured', e)