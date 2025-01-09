import streamlit as st
import utils as utl


def main():
    utl.load_datasets()

    #pagine del menù
    pages = {
        "Home": [st.Page("home.py", title = "Home", icon = "🏠")],
        "Analisi": [
            st.Page("app_pages/an_world.py", title = "Analisi nel Mondo", icon = "📊"),
            st.Page("app_pages/an_eu.py", title = "Analisi in Unione Europea", icon = "📊"),
            st.Page("app_pages/an_italy.py", title = "Analisi in Italia", icon = "📊")        
        ],
        "Quiz": [
            st.Page("quiz.py", title = "Quiz sulle Olimpiadi", icon = "❓")
        ],
        "Informazioni utili": [
            st.Page("information/info_data.py", title = "Dataset", icon = "📝"),
            st.Page("information/info_map.py", title = "Mappe", icon = "🗺️"), 
            st.Page("information/info_biblio.py", title = "Generali", icon = "📖"),      
        ],
    }

    #barra di navigazione
    st.session_state.pg = st.navigation(pages)
    st.session_state.pg.run()


if __name__ == "__main__":
    main()
