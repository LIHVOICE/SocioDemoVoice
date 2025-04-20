import streamlit as st
import pandas as pd
from utils.plot_helpers import generate_plotly_forest_plot
import os
from PIL import Image

# Folder containing the data
DATA_FOLDER = "regression data"
HEATMAP_FOLDER = "heatmaps"


# ----------------------
# Sidebar Menu
# ----------------------
st.sidebar.title("Forest Plot Visualizer 🌲")
st.sidebar.caption("Select parameters")
show_heatmap = st.sidebar.checkbox("Display Heatmap")

audio_types = ['reading', 'a_vowel phonation'] 
feature_set_reading = ['egemaps', 'articulation', 'phonological', 'phonation', 'prosody', 'glottal'] 
feature_set_phonation = ['egemaps', 'phonation', 'prosody', 'glottal'] 
socio_factors = socio_factors = ['age', 'surveyLocale', 'native', 'educ_years', 'smoking', 'alcohol'] 

# User input: select the sociodemographic variable

audio_type = st.sidebar.selectbox("Choose an audio type:", audio_types)
if audio_type == 'a_vowel phonation':
    audio_type = 'a_vowel'
    feature_set = st.sidebar.selectbox("Choose a feature set:", feature_set_phonation)
elif audio_type == 'reading':
    feature_set = st.sidebar.selectbox("Choose a feature set:", feature_set_reading)

socio_var = st.sidebar.selectbox("Choose a sociodemographic variable:", socio_factors)
gender_var = st.sidebar.selectbox("Choose gender variable:", ['female', 'male'])

filename = f'{audio_type}_{feature_set}_{gender_var}.npy'
feature_columns = f'{feature_set}_columns_to_work_with.npy'

if gender_var == 'female':
    gender_des = 'women'
elif gender_var == 'male':
    gender_des = 'men'

# ----------------------
# Main Area
# ----------------------

st.title(f"The effect of {socio_var} on the {feature_set} features for {gender_des} 📊 ")

# Generate plot
fig = generate_plotly_forest_plot(
    input_filename = os.path.join(DATA_FOLDER, filename),
    columns_to_work_with = os.path.join(DATA_FOLDER, feature_columns),
    socio_factors = socio_factors,
    coef_name = socio_var,
    feature_name = feature_set,
    gender = gender_var)

input_filename = f"{audio_type}_{feature_set}_{gender_var}_{socio_var}.jpg"
# Load an image using Pillow
heatmap_image = Image.open(os.path.join(HEATMAP_FOLDER, input_filename))

# Display
st.plotly_chart(fig, use_container_width=True)

if show_heatmap:
    img = Image.open("heatmap.jpg")
    st.image(img, use_container_width=True)

if "show_heatmap" not in st.session_state:
    st.session_state.show_heatmap = False

if st.button("Toggle Heatmap"):
    st.session_state.show_heatmap = not st.session_state.show_heatmap

if st.session_state.show_heatmap:
    st.image(heatmap_image, caption="Associated heatmap", use_container_width=True)