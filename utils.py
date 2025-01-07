import streamlit as st
from dataframes.medals import olympics
from dataframes.city import cities
from dataframes.italy2024 import italy
import dataframes.countries as countries
from PIL import Image
import geopandas as gpd
import os

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

def get_geography():
    path = "map/ne_10m_admin_0_countries.zip"
    return gpd.read_file(path)

def get_region():
    path = "map/ne_10m_admin_1_states_provinces.zip"
    return gpd.read_file(path)

def add_map(chart, name = "map"):
    chart.save(f"map/{name}.html")

def open_map(chart, name = "map"):
    path = f"map/{name}.html"
    if os.path.exists(path):
        with open(path) as fp:
            st.components.v1.html(fp.read(), width = 800, height = 600)
    else:
        add_map(chart, name)
        with open(path) as fp:
            st.components.v1.html(fp.read(), width = 800, height = 600)
