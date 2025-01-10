import streamlit as st
import polars as pl
import altair as alt
import utils as utl
import numpy as np

utl.setup_page(
    title = "Europa",
    icon = "🇪🇺",
    layout = "centered"
)

#import dataset
medals = st.session_state.medal
europe = st.session_state.europe
medals = medals.with_columns(
    pl.when(pl.col("Nation") == "West Germany")
    .then(pl.lit("Germany"))
    .otherwise(pl.col("Nation"))
    .alias("Nation")
)
medals = (medals
          .group_by(["Nation", "Year"])
          .agg([
              pl.col("Gold").sum().alias("Gold"),
              pl.col("Silver").sum().alias("Silver"),
              pl.col("Bronze").sum().alias("Bronze"),
              pl.col("Total").sum().alias("Total")
          ])
)
#medaglie europa
eu_medals = (
    medals
    .join(europe.rename({"Year": "eu_Year"}), on = "Nation", how = "left") 
    .filter(pl.col("Year") >= pl.col("eu_Year"))  
)

#titolo
st.title("Analisi delle medaglie olimpiche in Unione Europea 🤝")
#commento introduttivo
st.markdown(
    """
    <p>
    In questa pagina è possibile esplorare le performance delle nazioni dell'Unione Europea ai giochi olimpici. Attraverso grafici interattivi e mappe, 
    vengono analizzati le medaglie conquistate dai paesi membri, il loro contributo storico e l'evoluzione delle prestazioni nel tempo dopo il loro 
    ingresso nell'UE.
    <br>
    Per ragioni computazionali le medaglie della Germania Est e della Germania Ovest sono state unite e considerate come un'unica nazione. Inoltre si 
    è scelto di utilizzare il 1958 come data di ingresso nell'UE per la Germania anche se all'epoca il paese era diviso e solo la Germania Ovest 
    faceva parte dell'UE.
    <br>
    Per correttezza è giusto sottolineare che il dataset analizzato prende in considerazione le medaglie vinte dalle nazioni a partire dalla prima 
    edizione delle Olimpiadi in cui tali nazioni sono entrate nell'Unione Europea. Per esempio per la Spagna vengono considerate le medaglie vinte 
    alle Olimpiadi di Seoul 1988 e in tutte le edizioni successive visto che la Spagna è entrata nell'UE nel 1986.
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

#mappa paesi ue
st.markdown("""<h3> 🌍 Distribuzione geografica delle nazioni dell'UE </h3>""",
            unsafe_allow_html = True)
#descrizione
st.markdown(
    """
    <div class = "description">
    Questa mappa evidenzia i paesi aderenti all'Unione Europea e il colore indica l'anno in cui la nazione 
    è entrata nell'UE. In blu si possono notare i sei paesi fondatori: Germania, Francia, Italia, Paesi Bassi, Belgio e Lussemburgo.
    </div>
    """,
    unsafe_allow_html = True
)

#creo mappa del mondo e coloro di grigio chiaro
world = utl.get_geography()
chartwrl = (
    alt.Chart(world)
    .mark_geoshape()
    .encode(color = alt.value("lightgrey"))
    .properties(width = 600, height = 600)
)
#creo mappa dell'UE e differenzio per anno
eu_nations = world.merge(
    europe.to_pandas(),
    left_on = "ADMIN",
    right_on = "Nation"
)
charteu = (
    alt.Chart(eu_nations)
    .mark_geoshape()
    .encode(
        alt.Color("Year:O", 
                  scale = alt.Scale(scheme = "category10"), 
                  legend = alt.Legend(orient = "top"), 
                  title = "Anno")
    )
)
#mappa finale
chart = ((chartwrl + charteu )
         .properties(width = 600, height = 600)
         .project(
             type = "azimuthalEqualArea",
             scale = 800,
             center = (10, 48)
         )
)

utl.open_map(chart, "eu_year")

#europa alle Olimpiadi
st.markdown("""<h3> 🥇 Performance olimpiche totali delle nazioni </h3>""",
            unsafe_allow_html = True)
#descrizione
st.markdown(
    """
    <div class = "description">
    Il grafico a barre mostra il numero totale di medaglie olimpiche vinte da ciascuna nazione.
    </div>
    """,
    unsafe_allow_html = True
)

#creo grafico
medal_counts = (
    eu_medals
    .group_by("Nation")
    .agg([
        pl.col("Gold").sum().alias("Gold"),
        pl.col("Silver").sum().alias("Silver"),
        pl.col("Bronze").sum().alias("Bronze"),
        pl.col("Total").sum().alias("Total"),
        pl.col("eu_Year").min().alias("Year")])
    .sort("Total", descending = True)

)
chart = (
    alt.Chart(medal_counts)
    .mark_bar()
    .encode(
        alt.X("Nation:N", sort = "-y", title = "Nazioni"),
        alt.Y("Total:Q", title = "Totale medaglie"),
        alt.Color("Nation:N", title = "Nazioni", legend = None),
        tooltip = [
            alt.Tooltip("Nation:N", title = "Nazione"),
            alt.Tooltip("Gold:Q", title = "Ori"),
            alt.Tooltip("Silver:Q", title = "Argenti"),
            alt.Tooltip("Bronze:Q", title = "Bronzi"),
            alt.Tooltip("Total:Q", title = "Totale"),
            alt.Tooltip("Year:O", title = "Entrata in UE")
        ]
    )
    .properties(title = "Totale medaglie olimpiche per paese dell'UE",)
    .configure_title(anchor = "middle")
)

st.altair_chart(chart, 
                use_container_width = True)

#nazioni - medaglie
st.markdown("""<h3> ⚖️ Confronto tra le nazioni e tipoligia di medaglie </h3>""",
            unsafe_allow_html = True)

#lista nazioni
nations = eu_medals.select("Nation").unique().sort("Nation").to_series().to_list()

selected_nations = st.multiselect(
    "Seleziona uno o più stati",
    nations,
    max_selections = 3,
    default = ["Italy", "France", "Spain"]
)

#descrizione
st.markdown(
    """
    <div class = "description">
    Questo grafico confronta i tipi di medaglie vinte da un massimo di 3 nazioni selezionate. Ogni barra rappresenta il totale per una specifica 
    tipologia di medaglia e fornisce un'analisi comparativa visiva.
    </div>
    """,
    unsafe_allow_html = True
)

#creo grafico
chart_data = (medals
           .filter(pl.col("Nation").is_in(selected_nations))
           .group_by(["Nation"])
           .agg([
               pl.col("Gold").sum().alias("Gold"),
               pl.col("Silver").sum().alias("Silver"),
               pl.col("Bronze").sum().alias("Bronze"),
               pl.col("Total").sum().alias("Total")
           ])
           .select(["Nation", "Gold", "Silver", "Bronze"])
           .unpivot(
                index = "Nation",
                on = ["Gold", "Silver", "Bronze"],
                value_name = "Count",
                variable_name = "Type"
            )
)
chart = (alt.Chart(chart_data)
        .mark_bar(size = 40)
        .encode(
            alt.X("Nation:N"),
            alt.XOffset(
                "Type:N",
                title = "Tipo di Medaglia",
                sort = ["Silver", "Gold", "Bronze"]
            ),
            alt.Y("Count:Q", title = "Totale medaglie"),
            alt.Color(
                "Type:N",
                title = "Tipo di medaglia",
                scale = alt.Scale(domain = ["Gold", "Silver", "Bronze"], range = ["#FFD700", "#C0C0C0", "#CD7F32"])
            ),
            tooltip = [
                alt.Tooltip("Nation:N", title = "Nazione"),
                alt.Tooltip("Type:N", title = "Tipo di medaglia"),
                alt.Tooltip("Count:Q", title = "Quantità")
            ]
        )
        .properties(title = "Confronto tra nazioni e tipologia di medaglie")
        .configure_title(anchor = "middle")
)


st.altair_chart(chart, 
                use_container_width = True)

#heatmap
st.markdown("""<h3> 📊 Totale delle medaglie nel tempo </h3>""",
            unsafe_allow_html = True)

#descrizione
st.markdown(
    """
    <div class = "description">
    Questa heatmap visualizza l'andamento delle medaglie totali conquistate da ciascuna nazione dell'Unione Europea nel corso degli anni. 
    Le sfumature più scure indicano una maggiore quantità di medaglie permettendo di osservare i picchi nelle performance olimpiche 
    delle nazioni nel tempo.
    </div>
    """,
    unsafe_allow_html = True
)

#creo grafico
chart = (
    alt.Chart(eu_medals)
    .mark_rect()
    .encode(
        alt.X("Year:O", title = "Anno"),
        alt.Y("Nation:N", title = "Nazione"),
        alt.Color("Total:Q", scale = alt.Scale(type = "log", scheme = "bluepurple"), title = "Totale medaglie"),
        tooltip=[
            alt.Tooltip("Nation:N", title = "Nazione"),
            alt.Tooltip("Year:O", title = "Anno"),
            alt.Tooltip("Total:Q", title = "Totale medaglie")
        ]
    )
    .properties(title = "Totale medaglie per anno e nazione")
    .configure_title(anchor = "middle")
)

st.altair_chart(chart, 
                use_container_width = True)

#commento
st.markdown(
    """
    <div class = "description">
    Dalla heatmap emerge chiaramente che nazioni come Francia, Germania e Italia hanno un ruolo centrale nel medagliere totale dell'Unione Europea,
    infatti i loro colori sono molto intensi rappresendando così il loro costante successo olimpico nel corso degli anni. 
    Anche i Paesi Bassi pur partendo da una posizione meno prominente hanno mostrato un crescente impatto soprattutto nelle edizioni recenti
    dimostrando una crescente influenza sul totale delle medaglie.
    </div>
    """,
    unsafe_allow_html = True
)

#mappa delle medaglie
st.markdown("""<h3> 🗺️ Mappa geografica delle medaglie olimpiche </h3>""",
            unsafe_allow_html = True)

#descrizione
st.markdown(
    """
    <div class = "description">
    La mappa rappresenta il totale delle medaglie olimpiche vinte da ciascuna nazione europea. Il colore indica il numero totale di medaglie vinte da
    ciascuna nazione: le sfumature più scure che rappresentano performance più elevate. Utile per comprendere a livello visivo la distribuzione 
    geografica delle medaglie.
    </div>
    """,
    unsafe_allow_html = True
)

#creo livelli per le medaglie
bins = [0, 5, 10, 25, 50, 100, 250, 500, 750, np.inf]
labels = [">=0", ">=5", ">=15", ">=25", ">=30", ">=50", ">=75", ">=100", ">=300", ">=500"]
medals_data = medal_counts.with_columns(
    pl.when(pl.col("Total").is_between(0, 5)).then(pl.lit(">=0"))
    .when(pl.col("Total").is_between(5, 15)).then(pl.lit(">=5"))
    .when(pl.col("Total").is_between(15, 25)).then(pl.lit(">=15"))
    .when(pl.col("Total").is_between(25, 30)).then(pl.lit(">=25"))
    .when(pl.col("Total").is_between(30, 50)).then(pl.lit(">=30"))
    .when(pl.col("Total").is_between(50, 75)).then(pl.lit(">=50"))
    .when(pl.col("Total").is_between(75, 100)).then(pl.lit(">=75"))
    .when(pl.col("Total").is_between(100, 300)).then(pl.lit(">=100"))
    .when(pl.col("Total").is_between(300, 500)).then(pl.lit(">=300"))
    .when(pl.col("Total").is_between(500, np.inf)).then(pl.lit(">=500"))
    .otherwise(pl.lit("None"))
    .alias("Total_cat"))
medals_data = world.merge(
    medals_data.to_pandas(),
    left_on = "ADMIN",
    right_on = "Nation"
)

#creo mappa
charteu = (
    alt.Chart(medals_data)
    .mark_geoshape()
    .encode(
        alt.Color(
            "Total_cat:N", 
            scale = alt.Scale(domain = labels, range=[
            "#ffffff", "#ffebeb", "#ffcccc", "#ff9999", "#ff6666", 
            "#ff3333", "#ff0000", "#cc0000", "#990000", "#660000"
        ]),
            title = "Totale medaglie"
        )
    )
)
#mappa finale
chart = ((chartwrl + charteu )
         .properties(width = 600, height = 600)
         .project(
             type = "azimuthalEqualArea",
             scale = 800,
             center = (10, 48)
         )
)

utl.open_map(chart, "europe_medals")

st.markdown(
    """
    <div class = "description">
    La mappa evidenzia chiaramente il ruolo centrale di nazioni come Francia, Italia e Germania nel medagliere totale dell'Unione Europea.
    Questi paesi si distinguono per il loro costante successo olimpico nel corso degli anni. Al contrario è evidente come i paesi dell'Est Europa 
    abbiano avuto un impatto marginale sul totale delle medaglie. Questo suggerisce una partecipazione meno significativa da 
    parte di queste nazioni che non hanno raggiunto gli stessi livelli di performance degli altri paesi europei. Inoltre ci fa capire che se
    l'UE gareggiasse come entità unica alle Olimpiadi la somma delle medaglie di Francia, Italia e Germania rappresenterebbe 
    un blocco significativo per il successo olimpico.
    </div>
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