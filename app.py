import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pandas as pd
import pickle

# Load the trained model
model = tf.keras.models.load_model('model.h5')

# Load the encoder and scaler
with open('geo_encoder.pkl', 'rb') as file:
    geo_encoder = pickle.load(file)

with open('gender_encoder.pkl', 'rb') as file:
    gender_encoder = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)


# Streamlit App
st.title('Customer Churn Prediction, by Franck Binde')

st.write('This is an experimental project used to practice Artifical Neural Networks with Tensorflow.')

st.write('This app will help us determine whether a customer will churn, based on specific attibutes.')
st.write('Please, input your values from the options below.')

# User input
geography = st.selectbox('Geography', geo_encoder.categories_[0])
gender = st.selectbox('Gender', gender_encoder.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1 ,4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])


# Prepare the input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [gender_encoder.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})


# Encoding Geography

encoded_geo = geo_encoder.transform([[geography]]).toarray()
encoded_geo_df = pd.DataFrame(encoded_geo, columns=geo_encoder.get_feature_names_out(['Geography']))


input_data = pd.concat([input_data.reset_index(drop=True), encoded_geo_df], axis=1)

# Scale the input data
input_data_scaled = scaler.transform(input_data)

# Prediction

prediction = model.predict(input_data_scaled)
prediction_proba = prediction[0][0]

st.write("RESULTS:")
st.write("________")
st.write(f"Churn probability: {round(prediction_proba*100,1)}%.")
if prediction_proba > 0.5:
    st.write("The customer is likely to churn.")
else:
    st.write("The customer is NOT likely to churn.")












