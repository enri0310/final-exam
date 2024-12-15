import streamlit as st
import polars as pl
import altair as alt
import utils as utl

utl.setup_page(
    title="Italia",
    icon="🇮🇹",
    layout="centered"
)

st.title("Analisi delle Medaglie Olimpiche in Italia 🍕")

medals = st.session_state.medal

st.metric(
    label="Nazioni Partecipanti",
    value=None
)
st.metric(
    label="Nazioni Vincitrici",
    value=None
)

italy2024 = st.session_state.italy2024
italy2024
