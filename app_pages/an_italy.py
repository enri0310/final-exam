import streamlit as st
import polars as pl
import altair as alt
import utils as utl

utl.setup_page(
    title = "Italia",
    icon = "🇮🇹",
    layout = "centered"
)

#import dataset
medals = st.session_state.medal
medals = medals.filter(pl.col("Nation") == "Italy")
italy2024 = st.session_state.italy2024
df_allyears = pl.DataFrame({"Year": list(range(1896, 2025, 4))})

#lista delle regioni
regioni = italy2024.select("Region").unique().sort("Region").to_series().to_list()

#titolo
st.title("Analisi delle Medaglie Olimpiche in Italia 🍕")
#commento introduttivo
st.markdown(
    """
    <p>
    In questa pagina vengono analizzate le medaglie olimpiche ottenute dall'Italia nel corso della storia con un focus particolare sull'ultima edizione, 
    ovvero le Olimpiadi di Parigi 2024. È importante notare che nella sezione relativa alle medaglie vinte a Parigi il totale non corrisponde a 40, 
    bennsì a 87. Questo perché il dataset considera tutti gli atleti italiani medagliati individualmente. Ad esempio il bronzo vinto dalla staffetta 
    4x100m stile libero maschile non viene conteggiato come una sola medaglia, ma come quattro, poiché vengono inclusi i quattro atleti medagliati: 
    Thomas Ceccon, Alessandro Miressi, Paolo Conte Bonin e Manuel Frigo.
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

#italia alle Olimpiadi
st.markdown("""<h3> 🏅 Evoluzione delle medaglie olimpiche nel tempo </h3>""",
            unsafe_allow_html = True)
#descrizione
st.markdown(
    """
    <div class = "description">
    Questo grafico mostra l'evoluzione delle medaglie olimpiche vinte dall'Italia nel corso delle edizioni olimpiche. Le medaglie sono suddivise per tipo
    (oro, argento, bronzo) e visualizzate nel tempo, dal 1896 fino al 2024. Le aree colorate rappresentano la distribuzione di ciascun tipo di medaglia.
    </div>
    """,
    unsafe_allow_html = True
)

#creo grafico
data_chart = (df_allyears
              .join(
                  medals, 
                  on = "Year", 
                  how = "left"
               )
               .fill_null(0)
               .unpivot(
                   index = "Year",
                   on = ["Gold", "Silver", "Bronze"],
                   value_name = "Count",
                   variable_name = "Type"
               )
               .with_columns(
                   pl.when(pl.col("Type") == "Gold").then(1)
                   .when(pl.col("Type") == "Silver").then(2)
                   .when(pl.col("Type") == "Bronze").then(3)
                   .alias("Order")
               ) 
) 
chart = (alt.Chart(data_chart)
         .mark_area()
         .encode(
             alt.X("Year:O", axis = alt.Axis(labelAngle = -45), title = None),
             alt.Y("Count:Q", title = "Numero di medaglie"),
             alt.Color(
                     "Type:N", 
                     scale = alt.Scale(domain = ["Gold", "Silver", "Bronze"], range = ["#FFD700", "#C0C0C0", "#CD7F32"]),
                     legend = alt.Legend(orient = "top", title = None)
             ),
             alt.Order("Order:O", sort = "ascending")
         )
         .properties(
             title = "Evoluzione delle medaglie olimpiche italiane",
             height = 450)
         .configure_title(anchor = "middle")
)

st.altair_chart(chart, 
                use_container_width = True)

#commento
st.markdown(
    """
    <div class = "description">
    Dal grafico emerge un andamento piuttosto irregolare con fluttuazioni significative. Tuttavia se ci si concentra sulle ultime edizioni si osserva una 
    tendenza generale alla crescita che riguarda tutti i tipi di medaglia (oro, argento e bronzo). Questo suggerisce un miglioramento nelle performance 
    complessive nel tempo.
    </div>
    """,
    unsafe_allow_html = True
)


#grafico regioni medagliate
st.markdown("""<h3> 🌍 Distribuzione delle medaglie 2024 per regione </h3>""",
            unsafe_allow_html = True)
#descrizione
st.markdown(
    """
    <div class = "description">
    Questo grafico visualizza la distribuzione delle medaglie olimpiche italiane nelle diverse regioni nell'edizione di Parigi 2024. 
    Ogni barra rappresenta una regione e mostra il numero totale di medaglie conquistate suddivise per tipo (oro, argento, bronzo).
    L'ordinamento delle regioni è basato sull'importanza relativa del numero di medaglie ottenute da ciascuna regione, con le regioni più medagliate in 
    cima alla lista.
    </div>
    """,
    unsafe_allow_html = True
)

#dati regionali
region2024 = (
    italy2024
    .group_by("Region")
    .agg([
        pl.col("Gold").sum(),
        pl.col("Silver").sum(),
        pl.col("Bronze").sum(),
        pl.col("Total").sum()
    ])
)
sort_chart = (
    region2024
    .with_columns( 
        (pl.col("Total") * 10000000 +
         pl.col("Gold") * 100000 + 
         pl.col("Silver") * 100 + 
         pl.col("Bronze")).alias("Weight") 
    )
    .sort("Weight", descending=True) 
)
data_chart = (
    italy2024
    .group_by("Region")
    .agg([
        pl.col("Gold").sum(),
        pl.col("Silver").sum(),
        pl.col("Bronze").sum()
    ])
    .unpivot(
        index = "Region",
        on = ["Gold", "Silver", "Bronze"],
        value_name = "Count",
        variable_name = "Type"
    )
    .with_columns(
        pl.when(pl.col("Type") == "Gold").then(1)
        .when(pl.col("Type") == "Silver").then(2)
        .when(pl.col("Type") == "Bronze").then(3)
        .alias("Order")
    )
    .join(
        sort_chart.select(["Region", "Weight"]),
        on = "Region",
        how = "left"
    )
    .filter(pl.col("Count") > 0)
)

#creo grafico
bar_chart = (alt.Chart(data_chart)
             .mark_bar()
             .encode(
                 alt.X("Count:Q", title = "Numero di medaglie", stack = "zero"),
                 alt.Y("Region:N", sort = list(sort_chart["Region"]), title = None),
                 alt.Color(
                     "Type:N", 
                     scale = alt.Scale(domain = ["Gold", "Silver", "Bronze"], range = ["#FFD700", "#C0C0C0", "#CD7F32"]),
                     legend = alt.Legend(orient = "top", title = None)
                 ),
                 alt.Order("Order:O"),
                 tooltip = [
                     alt.Tooltip("Region:N", title = "Regione"),                   
                     alt.Tooltip("Type:N", title = "Tipologia"),
                     alt.Tooltip("Count:Q", title = "Numero")
                 ]
             )
)
text_chart = (alt.Chart(data_chart)
              .mark_text(dx = -5, fontWeight = "bold")
              .encode(
                  alt.X("Count:Q", stack = "zero"),
                  alt.Y("Region:N", sort = list(sort_chart["Region"])),
                  alt.Order("Order:O"),
                  detail = "Type:N",
                  text = alt.Text("Count:Q") 
              )
)
final_chart = (
    (bar_chart + text_chart) 
    .properties(title = "Distribuzione delle medaglie olimpiche 2024 per regione")
    .configure_title(anchor = "middle")  
)

st.altair_chart(final_chart,
                use_container_width = True)

#commento
st.markdown(
    """
    <div class = "description">
    La Lombardia si conferma una delle regioni più performanti con 7 ori, 6 argenti e 2 bronzi, dominando il medagliere italiano. Nonostante ciò anche 
    altre regioni hanno contribuito in modo significativo al successo olimpico. La Toscana con 4 ori e un totale di 12 medaglie e il Veneto con 2 ori e 
    9 medaglie complessive sono altri esempi di territori che hanno lasciato un segno importante. In più è interessante notare come anche atleti italiani
    nati all'estero abbiano contribuito al medagliere.
    </div>
    """,
    unsafe_allow_html = True
)

#mappa delle medaglie
st.markdown("""<h3> 🗺️ Distribuzione geografica delle medaglie 2024 </h3>""",
            unsafe_allow_html = True)
#descrizione
st.markdown(
    """
    <div class = "description">
    La prima mappa visualizza la distribuzione geografica delle medaglie ottenute dall'Italia a Parigi 2024, con l'eccezione delle 6 medaglie conquistate 
    da atleti italiani nati all'estero. Le città italiane sono rappresentate da punti colorati dove il colore riflette il numero totale di medaglie 
    ottenute. Questo permette di individuare le città che hanno contribuito maggiormente ai successi olimpici.
    <br>
    Nella seconda mappa le medaglie sono invece raggruppate per regione. Ogni regione è colorata in base al totale delle medaglie conquistate dai suoi atleti.
    </div>
    """,
    unsafe_allow_html = True
)


#df città italiane
city = pl.read_csv("map/comuni_geocoded.csv", null_values = ["NA", ""], separator = ";")
city = (
    city
    .group_by("nome")
    .agg([
        pl.col("nomeProvincia").first().alias("Provincia")
    ])
)
#lista province italiane
cities = city.select("Provincia").unique().to_series().to_list()
#province italiane
province = utl.get_region()
province = province[province["geonunit"] == "Italy"]
province["region"] = province["region"].str.lower()

#città medagliate 2024
town = (
    italy2024
    .filter(pl.col("Region") != "ESTERO")
    .group_by("City")
    .agg([
        pl.col("Gold").sum(),
        pl.col("Silver").sum(),
        pl.col("Bronze").sum(),
        pl.col("Total").sum()
    ])
)
#aggiungo province
town = town.join(
    city.select(pl.col("nome"), pl.col("Provincia")),
    how = "left",
    left_on = "City",
    right_on = "nome"
)

#province medagliate 2024
provincia = (
    town
    .group_by("Provincia")
    .agg([
        pl.col("Gold").sum(),
        pl.col("Silver").sum(),
        pl.col("Bronze").sum(),
        pl.col("Total").sum()
    ])
)
provincia = provincia.with_columns(
            pl.when(pl.col("Provincia") == "Torino")
            .then(pl.lit("Turin"))
            .when(pl.col("Provincia") == "Oristano")
            .then(pl.lit("Oristrano"))
            .when(pl.col("Provincia") == "Monza e della Brianza")
            .then(pl.lit("Monza e Brianza"))
            .otherwise(pl.col("Provincia"))
            .alias("Provincia")
        )
#lista province medagliate 2024
province_list = provincia.select("Provincia").unique().to_series().to_list()

#creo mappa
provincia = province.merge(
    provincia.to_pandas(),
    left_on = "name",
    right_on = "Provincia"
)

world = utl.get_geography()
#mappa italia
chartit = (
    alt.Chart(world[world["NAME"] == "Italy"])
    .mark_geoshape()
    .encode(color = alt.value("lightgrey"))
    .properties(width = 600, height = 600)
)
#mappa province
chartpr = (
    alt.Chart(provincia)
    .mark_circle(size = 20)
    .mark_geoshape()
    .encode(color = alt.Color("Total:N", scale = alt.Scale(scheme = "category10")))
    .properties(width = 600, height = 600)
)
#mappa finale
chart = ((chartit + chartpr)
         .properties(width = 600, height = 600)
         .project(
             type = "azimuthalEqualArea",
             scale = 2500, 
             center = (12, 42) 
         )
)

utl.open_map(chart, "province")

col1, col2 = st.columns(2)
with col1:
    st.metric(
        label = "Province medagliate",
        value = len(province_list)
    )
with col2:
    st.metric(
        label = "Province totali",
        value = len(cities)
    )

#regioni medagliate 2024
region2024 = region2024.with_columns(
            pl.when(pl.col("Region") == "SICILIA")
            .then(pl.lit("sicily"))
            .when(pl.col("Region") == "PUGLIA")
            .then(pl.lit("apulia"))
            .otherwise(pl.col("Region"))
            .alias("Region")
        )
region2024 = region2024.with_columns(pl.col("Region").str.to_lowercase().alias("Region"))

#creo mappa
region = province.merge(
    region2024.to_pandas(),
    left_on = "region",
    right_on = "Region"
)
#mappa regioni
chartrg = (
    alt.Chart(region)
    .mark_circle(size = 20)
    .mark_geoshape()
    .encode(color = alt.Color("Total:N", scale = alt.Scale(scheme = "category10")))
    .properties(width = 600, height = 600)
)
#mappa finale
chart = ((chartit + chartrg)
         .properties(width = 600, height = 600)
         .project(
             type = "azimuthalEqualArea",
             scale = 2500, 
             center = (12, 42) 
         )
)
utl.open_map(chart, "region")

col1, col2 = st.columns(2)
with col1:
    st.metric(
        label = "Regioni medagliate",
        value = len(regioni) - 1
    )
with col2:
    st.metric(
        label = "Regioni totali",
        value = 20
    )

#commento
st.markdown(
    """
    <div class = "description">
    Le due mappe fornite mettono in evidenza una marcata concentrazione di medaglie nelle regioni del Centro e Nord Italia, mentre le regioni del Sud 
    appaiono significativamente meno rappresentate. Questa disparità geografica suggerisce la possibilità di diversi fattori che potrebbero influenzare 
    la performance sportiva regionale. Potrebbe trattarsi di differenze nell'accesso alle risorse, come strutture sportive e 
    finanziamenti regionali o di fattori socio-culturali che incidono sulla partecipazione e la formazione degli atleti.  Un'analisi più approfondita 
    potrebbe consentire di indagare come questi fattori siano correlati e di esplorare in che misura influenzano le differenze regionali nella conquista
    delle medaglie olimpiche. 
    Per il momento ci limitiamo a evidenziare questa significativa discrepanza.
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