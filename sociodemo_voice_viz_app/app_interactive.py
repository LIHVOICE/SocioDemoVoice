import streamlit as st
import pandas as pd
from utils.plot_helpers import *
import os
from PIL import Image

# Folder containing the data
DATA_FOLDER = "regression data"
HEATMAP_FOLDER = "heatmaps"
SOCIO_VARIABLES = {
    'Age': 'age_group',
    'Language': 'surveyLocale',
    'Mother tongue': 'native',
    'Education level' : 'educ',
    'Smoking Status': 'smoking',
    'Alcohol Consumption': 'alcohol',   
}

# ----------------------
# Sidebar Menu
# ----------------------
st.sidebar.title("Visualization Controls 📊")
st.sidebar.caption("Select parameters")


audio_types = ['reading', 'a_vowel phonation'] 
feature_set_reading = ['egemaps', 'articulation', 'phonological', 'phonation', 'prosody', 'glottal'] 
feature_set_phonation = ['egemaps', 'phonation', 'glottal'] 
socio_factors = list(SOCIO_VARIABLES.keys())
audio_type = st.sidebar.selectbox("Choose an audio type:", audio_types)

tab1, tab2 = st.tabs(["Forest Plots", "More visualization"])

with tab1:

    if audio_type == 'a_vowel phonation':
        audio_type = 'a_vowel'
        feature_set = st.sidebar.selectbox("Choose a feature set:", feature_set_phonation)
    elif audio_type == 'reading':
        feature_set = st.sidebar.selectbox("Choose a feature set:", feature_set_reading)

    socio_var = st.sidebar.selectbox("Choose a sociodemographic variable:", socio_factors)
    gender_var = st.sidebar.selectbox("Choose gender:", ['female', 'male'])

    filename = f'{audio_type}_{feature_set}_{gender_var}.npy'
    feature_columns = f'{feature_set}_columns_to_work_with.npy'

    if gender_var == 'female':
        gender_des = 'women'
    elif gender_var == 'male':
        gender_des = 'men'

    # ----------------------
    # Main Area
    # ----------------------

    st.title(f"The effect of {socio_var} on the {feature_set} features")

    # Generate plot
    fig = generate_plotly_forest_plot(
        input_filename = os.path.join(DATA_FOLDER, filename),
        columns_to_work_with = os.path.join(DATA_FOLDER, feature_columns),
        socio_factors = socio_factors,
        coef_name = socio_var,
        feature_name = feature_set,
        gender = gender_var)
    # Display
    st.plotly_chart(fig, use_container_width=True)


with tab2:

    try:

        if socio_var in ['Age', 'Education level', 'Smoking Status']:

            fig = generate_plotly_heatmap(
                gender=gender_var,
                audio_type=audio_type,
                feature_name=feature_set,
                coef_name=SOCIO_VARIABLES[socio_var]
            )

        else:

            fig = generate_plotly_barplot(
                gender=gender_var,
                audio_type=audio_type,
                feature_name=feature_set,
                coef_name=SOCIO_VARIABLES[socio_var]
            )

        st.title(f"Significantly different {feature_set} features between {socio_var} groups")
        fig.update_traces(textfont_size=14)
        st.plotly_chart(fig, use_container_width=True)

    except:
        st.error(f"There is no significantly different {feature_set} features between {socio_var} value groups")

