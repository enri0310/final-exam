import streamlit as st
import utils as utl

# Caricamento iniziale
if __name__ == "__main__":
    utl.load_datasets()

    # Pagine del menu
    pages = {
        "Home": [st.Page("home.py", title="Home", icon="🏠")],
        "Analisi": [
            st.Page("app_pages/an_world.py", title="Analisi nel Mondo", icon="📅"),
            st.Page("app_pages/an_eu.py", title="Analisi in Unione Europea", icon="📅"),
            st.Page("app_pages/an_italy.py", title="Analisi in Italia", icon="📅")        
        ],
        "Quiz": []
    }

    st.session_state.pg = st.navigation(pages)
    st.session_state.pg.run()
