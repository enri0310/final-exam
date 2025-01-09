import streamlit as st
import utils as utl

utl.setup_page(
    title = "Olimpiadi",
    icon = "🏅",
    layout = "centered"
)

#immagine anelli
col1, col2, col3 = st.columns([2, 2, 2])
with col2:
    st.image(
        "images/logo.svg",
        use_container_width = True
    )

#titolo e sottotitolo
st.title("Gloria e medaglie: scopri le prestazioni olimpiche delle nazioni")
st.markdown(
    "<h3> Un viaggio attraverso i successi delle nazioni nelle Olimpiadi estive, dal passato glorioso al presente </h3>",
    unsafe_allow_html = True
)
#descrzione
st.markdown(
    """
    <p>
    Benvenuto! Questa piattaforma è dedicata a esplorare i medaglieri delle Olimpiadi estive, 
    una celebrazione dello sport che unisce atleti e nazioni da tutto il mondo.
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


#definizione
st.markdown("""<h3> 📚 Definizione di 'Olimpiade' </h3>""",
            unsafe_allow_html = True)
st.markdown("""
    <div>
    <strong>Olimpìade</strong>  s. f. [dal lat. <em>Olympias -iădis</em>, gr. <em>᾿Ολυμπιάς -άδος</em>] -
    <span style = "color: #808080;">1. In età antica: a. Complesso di gare (ginniche, atletiche, ippiche) che si celebravano ogni quattro anni 
    nella città greca di Olimpia, nell’Elide, in occasione delle feste olimpie, a partire dal 776 a. C. e fino al 393 d. C. b. Periodo di 
    tempo di quattro anni che intercorreva fra due successive celebrazioni delle feste e delle gare olimpie; usata fin dal sec. 5° come punto 
    di riferimento cronologico, l’olimpiade fu adottata come base di computo per la datazione ufficiale dallo storico Timeo e divulgata da 
    Eratostene (per es.: la prima o., il 776 a. C.; la seconda o., il 772 a. C., ecc.). 
    </span>
    2. In età moderna (per lo più al plur., le olimpiadi, e spesso con iniziale maiuscola), la più importante manifestazione sportiva per atleti 
    non professionisti, consistente in un complesso di gare internazionali, ispirate agli antichi giochi olimpici, che dal 1896 si svolgono 
    ogni quattro anni in sede diversa: le O. di Atene, di Roma, di Monaco, di Mosca, di Pechino. Dal 1924 si svolgono inoltre le o. invernali,
    anch’esse ogni quattro anni, che sono dedicate agli sport della neve e del ghiaccio e hanno luogo in un paese diverso da quello che 
    organizza i giochi olimpici, con uno scarto di due anni rispetto a questi ultimi.
    <div style = "text-align: right;"> 
    - <a href = "https://www.treccani.it/vocabolario/olimpiade/">Enciclopedia Treccani</a>
    </div>
    <br>
    </div>
    """, 
    unsafe_allow_html = True)


#pagine 'ANALISI'
st.markdown("""<h3> 🌍 Esplora i medaglieri </h3>""",
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Scopri le sezioni principali per analizzare i dati delle Olimpiadi estive.
    </p>
    """,
    unsafe_allow_html = True
)

col1, col2, col3 = st.columns(3)
with col1:
    st.image("images/medal_table.png", use_container_width = False)
    if st.button("Vai a medaglie nel Mondo"):
        st.switch_page("app_pages/an_world.py")
with col2:
    st.image("images/europe.png", use_container_width = False)
    if st.button("Vai a Medaglie in Europa"):
        st.switch_page("app_pages/an_eu.py")
with col3:
    st.image("images/medal.webp", use_container_width = False)
    if st.button("Vai a medaglie in Italia"):
        st.switch_page("app_pages/an_italy.py")

#esplora
st.markdown("""<h3>💬 Esplora, scopri, condividi</h3>""", 
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Questa piattaforma è il punto di partenza per scoprire storie e curiosità sulle Olimpiadi. 
    Naviga tra i dati, approfondisci i successi delle nazioni e lasciati ispirare dal mondo dello sport.
    </p>
    """,
    unsafe_allow_html = True)

#fonti
st.markdown("""<h3>📌 Fonti</h3>""",
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Le informazioni sui medaglieri sono state raccolte da dati pubblici disponibili su 
    <a href = "https://en.wikipedia.org/wiki/Main_Page">Wikipedia</a>.
    <br>
    Per trasparenza e per permettere ulteriori analisi è possibile scaricare tutti i file CSV utilizzati in un unico archivio. Per maggiori dettagli 
    consulta la pagina dedicata.
    </p>
    """,
    unsafe_allow_html = True
)

col1, col2 = st.columns([1, 2])
#zip dei dataset
with col1:
    with open("dataframes/dataframes.zip", "rb") as fp:
        btn = st.download_button(
            label = "📂 Scarica i dati",
            data = fp,
            file_name = "dataframes.zip",
            mime = "application/zip",
            use_container_width = True
        )
#pagina con informazioni
with col2:
    if st.button("ℹ️ Ulteriori informazioni"):
        st.switch_page("information/info_data.py")


st.markdown(
    """
    <br>
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
