import streamlit as st
from dataframes.medals import olympics
from dataframes.city import cities
import dataframes.countries as countries
from PIL import Image
import utils_pl as utlpl

#caricamento dei dataset nella sessione di lavoro
def load_datasets():
    st.session_state.medal = olympics()
    st.session_state.city = cities()
    st.session_state.europe = countries.europe()
    st.session_state.soviet = countries.get_soviet()
    st.session_state.yugoslavia = countries.get_yugoslavia()

#configurazione della pagina e caricamento css
def setup_page(title, icon, layout="centered", css_file = "style/style.css"):
    st.set_page_config(
        page_title = title,
        page_icon = icon,
        layout = layout
    )
    local_css("style/style.css")

def local_css(file):
    with open(file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#riduzione dimensione immagine
def resize_image(image_path, width, height):
    img = Image.open(image_path)
    return img.resize((width, height))

def unify_nation(df, renamed_dict):
    return utlpl.rename_nations(df, renamed_dict)


