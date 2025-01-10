import streamlit as st
from dataframes.medals import olympics
from dataframes.city import cities
from dataframes.italy2024 import italy
import dataframes.countries as countries
import geopandas as gpd
import os

#carica dataset nella sessione della pagina
def load_datasets():
    st.session_state.medal = olympics()
    st.session_state.city = cities()
    st.session_state.europe = countries.europe()
    st.session_state.soviet = countries.get_soviet()
    st.session_state.italy2024 = italy()

#set della pagina
def setup_page(title, icon, layout = "centered", css_file = "style/style.css"):
    st.set_page_config(
        page_title = title,
        page_icon = icon,
        layout = layout
    )
    local_css(css_file)

#apre file CSS
def local_css(file):
    with open(file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#ottinene mappa paesi
def get_geography():
    path = "map/ne_10m_admin_0_countries.zip"
    return gpd.read_file(path)

#ottiene mappa province
def get_region():
    path = "map/ne_10m_admin_1_states_provinces.zip"
    return gpd.read_file(path)

#salva mappa
def add_map(chart, name = "map"):
    chart.save(f"map/{name}.html")

#apre mappa
def open_map(chart, name = "map"):
    path = f"map/{name}.html"
    if os.path.exists(path):
        with open(path) as fp:
            st.components.v1.html(fp.read(), width = 800, height = 600)
    else:
        add_map(chart, name)
        with open(path) as fp:
            st.components.v1.html(fp.read(), width = 800, height = 600)
