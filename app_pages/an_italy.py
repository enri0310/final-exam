import streamlit as st
import polars as pl
import altair as alt
import utils as utl

utl.setup_page(
    title="Italia",
    icon="🏅",
    layout="centered",
    css_file="styles.css"
)

st.title("Analisi delle Medaglie Olimpiche in Italia")

medals = st.session_state.medal