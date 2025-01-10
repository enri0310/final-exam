import streamlit as st
import utils as utl

utl.setup_page(
    title = "Mappe",
    icon = "📍",
    layout = "centered"
)

st.title("Informazioni utili sui sulle mappe utlizzate 🧭")


st.markdown(
    """
    <hr style = "margin-top: 0; margin-bottom: 0; height: 2px; border: none; background-color: #1f77b4;">
    <br>
    """, 
    unsafe_allow_html = True
)


st.markdown("""<h3> 🔗 Fonti </h3>""",
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Per gestire i dati spaziali è stata utilizzata la libreria <b>geopandas</b>, che consente di rappresentare 
    le informazioni in un DataFrame con una colonna speciale dedicata alla geometria spaziale.
    In questa applicazione web i dati geografici sono stati ottenuti dal sito ufficiale <a href="https://www.naturalearthdata.com/">Natural Earth</a>. 
    Per migliorare l'efficienza del caricamento questi dati sono stati scaricati preventivamente e salvati nella cartella "<b>map</b>".
    </p>
    """,
    unsafe_allow_html = True
)


st.markdown("""<h3> 🌍 Visualizzazione delle mappe </h3>""",
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    La visualizzazione delle mappe in Streamlit può risultare complessa e richiede un encoding specifico.
    Per includere una mappa, è necessario salvarla prima in un file HTML e successivamente caricarla utilizzando 
    la funzione: <code>st.components.v1.html()</code>. Questo processo può essere oneroso in termini di tempo e risorse computazionali, soprattutto su 
    macchine meno performanti. Per ottimizzare questa operazione, le mappe generate vengono salvate nella cartella "<b>map</b>".
    Se la mappa è già presente, viene caricata direttamente senza dover ripetere il salvataggio.
    </p>
    """,
    unsafe_allow_html = True
)


st.markdown("""<h3> 🏞️ Mappa dell'Italia </h3>""",
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Per creare una mappa dettagliata dell'Italia, è stato utilizzato il dataset disponibile nel seguente repository GitHub:
    <a href = "https://github.com/gnekt/geolocalizzazione-comuni-italiani">geolocalizzazione dei comuni</a>.
    Questo dataset include informazioni sui comuni italiani come coordinate geografiche e dettagli amministrativi
    utili per rappresentare la distribuzione geografica a livello locale e provinciale. Quindi con l'aiuto della libreria <b>geopandas</b>, 
    i dati del repository sono stati caricati e manipolati per generare una visualizzazione specifica per il territorio italiano.
    </p>
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