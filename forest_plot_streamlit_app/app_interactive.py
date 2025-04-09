import streamlit as st
import pandas as pd
from utils.plot_helpers import generate_plotly_forest_plot
import os

# Folder containing the data
DATA_FOLDER = "data"

# ----------------------
# Sidebar Menu
# ----------------------
st.sidebar.title("Forest Plot Visualizer 🌲")
st.sidebar.caption("Select parameters")
# User input: select the sociodemographic variable
audio_types = ['reading', 'a_vowel phonation'] 
feature_set_reading = ['egemaps', 'articulation', 'phonological', 'phonation', 'prosody', 'glottal'] 
feature_set_phonation = ['egemaps', 'phonation', 'prosody', 'glottal'] 
socio_factors = ['age', 'gender', 'language', 'smoking', 'alcohol', 'education_years', 'speaking_native_tongue' ] 

audio_type = st.sidebar.selectbox("Choose an audio type:", audio_types)
if audio_type == 'a_vowel phonation':
    feature_set = st.sidebar.selectbox("Choose a feature set:", feature_set_phonation)
elif audio_type == 'reading':
    feature_set = st.sidebar.selectbox("Choose a feature set:", feature_set_reading)

socio_var = st.sidebar.selectbox("Choose a sociodemographic variable:", socio_factors)
gender_var = st.sidebar.selectbox("Choose gender variable:", ['both', 'male', 'female'])

#choose_feature_type
#choose_gender

# ----------------------
# Main Area
# ----------------------
st.title("📊 Forest Plot Explorer")

# Generate plot
fig = generate_plotly_forest_plot(
    input_filename = os.path.join(DATA_FOLDER, 'egemaps_median_regression_coefficients_both_genders.npy'),
    columns_to_work_with = os.path.join(DATA_FOLDER, 'egemaps_columns_to_work_with.npy'),
    socio_factors = socio_factors,
    coef_name = socio_var,
    feature_name = feature_set,
    gender = gender_var)

# Display
st.plotly_chart(fig, use_container_width=True)
