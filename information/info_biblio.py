import streamlit as st
import utils as utl

utl.setup_page(
    title = "Generale",
    icon = "⚙️",
    layout = "centered"
)

st.title("Informazioni generali 🖥️")


st.markdown(
    """
    <hr style = "margin-top: 0; margin-bottom: 0; height: 2px; border: none; background-color: #1f77b4;">
    <br>
    """, 
    unsafe_allow_html = True
)


st.markdown("""<h3> 📚 Bibliografia </h3>""", 
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    La bibliografia per il progetto include le seguenti fonti:
    </p>

    <ul>
        <li><b>Dispense dei corsi:</b> SISTEMI DI ELABORAZIONE 2, SISTEMI DI ELABORAZIONE 1, STRUTTURE DATI E PROGRAMMAZIONE e MODELLI STATISTICI 2;</li>
        <li><a href = "https://www.geeksforgeeks.org/">GeeksforGeeks</a> in particolare per le librerie RegEx, Statsmodels e Numpy;</li>
        <li><a href = "https://www.w3schools.com/">W3Schools</a> per la parte di HTML e CSS;</li>
        <li><b>Siti ufficiali delle librerie utilizzate</b>;</li>
        <li><a href="https://streamlit.io/gallery">Streamlit Gallery</a> per prendere ispirazione su font, colori e design da utilizzare;</li>
        <li><a href = "https://medium.com/@fesomade.alli/building-a-quiz-app-in-python-using-streamlit-d7c1aab4d690">Articolo</a> per la creazione del quiz.</li>
        
    </ul>
    """,
    unsafe_allow_html = True
)


st.markdown(
    """
    <hr style = "margin-top: 0; margin-bottom: 0; height: 2px; border: none; background-color: #1f77b4;">
    <br>
    """, 
    unsafe_allow_html = True
)


st.markdown("""<h3> 📦 Librerie utilizzate </h3>""", 
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Le principali librerie utilizzate per questo progetto sono:
    </p>

    <ul>
    <li><a href = "https://streamlit.io/">Streamlit</a>;</li>
    <li><a href = "https://pola.rs/">Polars</a>;</li>
    <li><a href = "https://altair-viz.github.io/">Altair</a>;</li>
    <li><a href = "https://pandas.pydata.org/">Pandas</a>;</li>
    <li><a href = "https://geopandas.org/en/stable/">Geopandas</a>;</li>
    <li><a href = "https://numpy.org/doc/">Numpy</a>;</li>
    <li><a href = "https://posit-dev.github.io/great-tables/articles/intro.html">great_tables</a>;</li>
    <li><a href = "https://www.statsmodels.org/stable/api.html">Statsmodels</a>;</li>
    <li><a href = "https://docs.python.org/3/library/re.html">RegEx</a>;</li>
    <li><a href = "https://docs.python.org/3/library/os.html">OS</a>;</li>
    <li><a href = "https://pypi.org/project/requests/">Requests</a>.</li>
    </ul>
    """,
    unsafe_allow_html = True
)


st.markdown("""<h3> 🔧 Utility </h3>""", 
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Per organizzare le funzioni utili al programma, sono stati creati due file Python:
    </p>

    <ul>
    <li><b>utils.py</b> che contiene le funzioni principali per l'interazione con <b>Streamlit</b>;</li>
    <li><b>utils_pl.py</b> che contiene funzioni utili in <b>Polars</b> per la creazione dei dataset.</li>
    </ul>
    """,
    unsafe_allow_html = True
)


st.markdown("""<h3> 🔗 Fonti </h3>""",
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Tutti i dataset utilizzati son stati creati o scaricati dalle seguenti fonti affidabili:
    </p>

    <ul>
    <li><a href = "https://en.wikipedia.org/wiki/Main_Page">Wikipedia</a>;</li>
    <li><a href = "https://www.naturalearthdata.com/">Natural Earth</a>;</li>
    <li><a href = "https://github.com/gnekt/geolocalizzazione-comuni-italiani">Geolocalizzazione dei comuni</a>;</li> 
    <li><a href = "https://www.eurosport.it/olimpiadi/olimpiadi-parigi-2024/2024/giochi-olimpici-italia-da-quali-regioni-arrivano-le-40-medaglie_sto20028615/story.shtml">Eurosport</a>.</li>       
    </ul>

    """,
    unsafe_allow_html = True
)


st.markdown(
    """
    <hr style = "margin-top: 0; margin-bottom: 0; height: 2px; border: none; background-color: #1f77b4;">
    <br>
    """, 
    unsafe_allow_html = True
)


#footer
st.markdown(
    """
    <div class = "footer">
    Creato con ❤️ da <b>Enrico Sorgato</b> © 2025
    </div>
    """,
    unsafe_allow_html = True
)