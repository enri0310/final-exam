import streamlit as st
import utils as utl

# Caricamento iniziale
if __name__ == "__main__":
    utl.load_datasets()

    # Pagine del menu
    pages = {
        "Home": [st.Page("home.py", title="Home", icon="🏠")],
        "Analisi": [
            st.Page("app_pages/an_nation.py", title="Analisi per nazione", icon="📅"),
            st.Page("app_pages/an_edition.py", title="Analisi per edizione", icon="📅"),
            st.Page("app_pages/an_eu.py", title="Analisi Unione Europea", icon="📅"),
        ],
        "Quiz": []
    }

    st.session_state.pg = st.navigation(pages)
    st.session_state.pg.run()
