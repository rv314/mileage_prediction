import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import pandas as pd
import os
import sys
import numpy as np


# Use the full page instead of a narrow central column
st.set_page_config(page_title = "Visualizations", layout="wide")

sys.path.insert(0, '/MPG_PRED')
st.sidebar.header("Visualizations")

def hide_footer():
  hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
  st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_footer()
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
  # Correlation Heatmap (Plotly)
  data_corr = mpg_data.corr()
  fig_1 = go.Figure()
  fig_1.add_trace(
    go.Heatmap(
        x = mpg_data.columns,
        y = data_corr.index,
        z = np.array(data_corr),
        text = data_corr.values,
        texttemplate='%{text:.2f}'))

  # Correlation Heatmap (Seaborn)
  plt.figure(figsize=(10,7))
  sns.heatmap(mpg_data.corr(), cmap=plt.cm.Reds, annot=True)
  plt.title('Correlation (relationship) between variables')

  # Scatter plot matrix
  fig_3 = px.scatter_matrix(mpg_data,
                          dimensions=['horsepower', 'weight','displacement'],
                          color='mpg')
except Exception as e:
  st.write('An error has occured', e)

# Space out the maps so the first one is 2x the size of the other three

# Heatmaps

with st.expander("Correlation Matrix", expanded=True):
    c1, c2 = st.columns((3, 2))
    st.write('''

      * Above correlation plots show evidence that there is correlation between our intended target variables and other independent variables.
      * Negative correlation is seen between few variables like displacement, horsepower etc and mpg, which suggests that mpg decreases as these variables increase.

    ''')
    with c1:
      st.header("Relationship between variables")
      st.plotly_chart(fig_1, use_container_width=True)

    with c2:
      st.header("")
      st.pyplot(plt)

# c3 = st.columns([2])

# Scatter Plot

with st.expander("Scatter Plot Matrix", expanded=True):
  #with c3:
  st.header("Relationship between variables (Scatter Plot)")
  st.plotly_chart(fig_3, use_container_width=True)
  st.write('''
      * We can confirm by seeing above that there is a negative correlation between mpg and displacement, horsepower and weight.
    ''')

# Data distribution

with st.expander("Bar Charts", expanded=True):
  c4, c5 = st.columns((2, 2))
  with c4:
    st.subheader("Count of data based on origin and cylinders")
    fig_5 = plt.figure(figsize=(3,4))
    fig_5 = pd.value_counts(mpg_data['origin']).plot.bar()
    fig_5.set_xlabel('Origin')
    fig_5.set_ylabel('Count')
    st.pyplot(plt)
  with c5:
    
    fig_6 = plt.figure(figsize=(3,4.2))
    fig_6 = pd.value_counts(mpg_data['cylinders']).plot.bar()
    fig_6.set_xlabel('Cylinders')
    fig_6.set_ylabel('Count')
    st.pyplot(plt)
  st.write('''
      * In this dataset, 'origin' column has values 1, 2 and 3. Where 1 is 'American' made car, 2 is 'European' car and 3 is 'Asian or other'. 
      * As seen in left bar chart, most cars are made in USA.
    ''')

# Box plots

with st.expander("Box Plots", expanded=True):
  st.header('Miles per gallon of cars based on origin')
  fig_6 = px.box(mpg_data, x='origin', y='mpg', color='origin', points='all')
  st.plotly_chart(fig_6, use_container_width=True)
  st.write('* We can see from above that cars made in Asian or other countries (origin=3) seem to be having higher mileage (As per the dataset).')

# Data distribution (Histogram)

with st.expander("Histogram", expanded=True):
  st.header('Distribution of data (mpg records)')
  fig_7 = px.histogram(mpg_data, x='mpg', text_auto=True)
  st.plotly_chart(fig_7, use_container_width=True)
  st.write('* Seems to be skewed, so most of the cars in this dataset have fuel efficiency of range 15-30.')