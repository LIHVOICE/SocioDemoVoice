import streamlit as st
import os
from PIL import Image

# App title
st.set_page_config(page_title="Feature Forest", layout="wide")
st.title("🌳 Forest Plots by Sociodemographic Characteristics")

# Folder containing the images
IMAGE_FOLDER = "images"

# List of characteristics to show (match filenames)
characteristics = {
    "Age Group": "forest_plot_age_egemaps_both_genders.png",
    "Gender": "forest_plot_gender_egemaps_both_genders.png",
    "Education Level": "forest_plot_educ_years_egemaps_both_genders.png",
    "Native tongue": "forest_plot_native_egemaps_both_genders.png"
}

# Sidebar for navigation
st.sidebar.title("Select Characteristic")
selected = st.sidebar.radio("Choose one:", list(characteristics.keys()))

# Load and display the image
image_path = os.path.join(IMAGE_FOLDER, characteristics[selected])
if os.path.exists(image_path):
    image = Image.open(image_path)
    st.image(image, caption=f"Forest Plot - {selected}", use_column_width=True)
else:
    st.error(f"Image not found for {selected}.")

# Optional: add about section
with st.expander("ℹ️ About this app"):
    st.markdown("""
        This interactive app displays forest plots showing how different features relate to various sociodemographic groups. 
        Each image visualizes regression coefficients or effect sizes for a specific grouping variable.
    """)
