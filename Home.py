from copyreg import pickle
from datetime import datetime
import pickle as pk
import streamlit as st
import os
import time
import sklearn

st.set_page_config("Prediction of fuel consumption", layout="wide")

st.sidebar.header('Navigation Menu ☝️')
st.sidebar.success('Welcome 👋')

def data_tranform(year, origin, fuel, count=2):
  year_digit = None
  origin_num = None
  fuel_num = None
  
  year_digit = abs(year) % (10**count)
  
  if origin == 'American':
    origin_num = 1
  elif origin == 'European':
    origin_num = 2
  else:
    origin_num = 3
  
  if fuel == 'Diesel':
    fuel_num = 1
  else:
    fuel_num = 0

  return year_digit, origin_num, fuel_num

def get_origin_num(value):
  if value == 'American':
    return 1
  elif value == 'European':
    return 2
  else:
    return 3

def predict(data):

  base_models = './models/'
  model_file = 'xgb_model.sav'
  xmodel = os.path.join(os.path.dirname(base_models), model_file)

  # Model
  model = None
  with open(xmodel, 'rb') as m:
    model = pk.load(m)

  return model.predict(data)

def hide_footer():
  hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
  st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():

  # Set title

  st.markdown("<h1 style='text-align: center; color: white;'>Prediction of fuel efficiency</h1>", unsafe_allow_html=True)

  # st.write('The scikit-learn version is {}.'.format(sklearn.__version__))
  hide_footer()

  with st.container():

    cylinders = st.number_input("Cylinders (range[1-16])", min_value = 1, max_value = 16)
    displacement = st.number_input("Displacement (range[60-450])", min_value = 60, max_value = 450)
    horsepower = st.number_input("Horsepower (range[50-230]", min_value = 50, max_value = 230)
    weight = st.number_input("Weight (range[1600-5000]", min_value = 1600, max_value = 5000)
    acceleration = st.number_input("Acceleration (range[8.0-25.0]", min_value = 8.0, max_value = 25.0)
    model_year = st.selectbox("Model Year", range(1990, 2024))
    origin = st.selectbox("Origin", ('American', 'European', 'Asian / Other'))
    car_type = st.selectbox("Fuel Type", ('Diesel', 'Non-Diesel'))


    if st.button('Predict 🔍'):

      try:
        # Perform transformations
        model_year_num, origin_num, car_type_num = data_tranform(model_year, origin, car_type)

        # Pass data to model function
        fuel_efficiency = predict([[cylinders, displacement, horsepower, weight, acceleration, model_year_num, origin_num, car_type_num]])

        # Round the results
        fuel_efficiency = str(round(fuel_efficiency[0], 2))

        with st.spinner('Analyzing... '):
          time.sleep(1)

        st.subheader("----- Prediction -----")
        st.write(f'This car has a fuel efficiency of {fuel_efficiency} MPG.')
        st.subheader("----- Model Details -----")
        st.write(f'This model was trained using Extreme Gradient Boosting Algorithm (XGB).')
        st.subheader("----- Evaluation Metrics -----")
        st.write(f'RMSE :  2.78')
        st.write(f'Model accuracy: 89.32%')

      except Exception as e:
        st.write("An error has occured: ", e)
      

if __name__ == "__main__":
  main()