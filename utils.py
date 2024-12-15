import streamlit as st
from dataframes.medals import olympics
from dataframes.city import cities
from dataframes.italy2024 import italy
import dataframes.countries as countries
from PIL import Image

def load_datasets():
    st.session_state.medal = olympics()
    st.session_state.city = cities()
    st.session_state.europe = countries.europe()
    st.session_state.soviet = countries.get_soviet()
    st.session_state.yugoslavia = countries.get_yugoslavia()
    st.session_state.italy2024 = italy()

def setup_page(title, icon, layout = "centered", css_file = "style/style.css"):
    st.set_page_config(
        page_title = title,
        page_icon = icon,
        layout = layout
    )
    local_css(css_file)

def local_css(file):
    with open(file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

def resize_image(image_path, width, height):
    img = Image.open(image_path)
    return img.resize((width, height))



