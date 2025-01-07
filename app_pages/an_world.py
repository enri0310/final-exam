import streamlit as st
import polars as pl
import altair as alt
import utils as utl
import polars.selectors as cs
from great_tables import loc, style, GT, md
import numpy as np
import statsmodels.api as sm

utl.setup_page(
    title = "Mondo",
    icon = "🌍",
    layout = "centered"
)

#import dataset
medals = st.session_state.medal
medals = medals.with_columns(pl.col("Nation").alias("old_nation"))
cities = st.session_state.city
cities = cities.with_columns(
    pl.col("Nation").alias("old_nation")
)
#caso della germania est e ovest
with st.sidebar:
    if st.toggle("Unisci Germania Est ed Ovest", value=False):
        medals = medals.with_columns(
            pl.when(pl.col("Nation") == "East Germany")
            .then(pl.lit("Germany"))
            .when(pl.col("Nation") == "West Germany")
            .then(pl.lit("Germany"))
            .otherwise(pl.col("Nation"))
            .alias("Nation")
        )
        cities = cities.with_columns(
            pl.when(pl.col("Nation") == "West Germany")
            .then(pl.lit("Germany"))
            .otherwise(pl.col("Nation"))
            .alias("Nation")
        )
    else:
        medals = medals.with_columns(pl.col("old_nation").alias("Nation"))
        cities = cities.with_columns(pl.col("old_nation").alias("Nation"))
medals = (medals
              .group_by(["Nation", "Year"])
              .agg([pl.col("Gold").sum().alias("Gold"),
                    pl.col("Silver").sum().alias("Silver"),
                    pl.col("Bronze").sum().alias("Bronze"),
                    pl.col("Total").sum().alias("Total")]
              )
)

st.title("Analisi delle medaglie olimpiche nel Mondo 🌍")

#commento introduttivo
st.markdown(
    """
    <p>
    In questa pagina è pissibile esplorare le performance delle nazioni in ogni edizione dei giochi olimpici. Sono presenti due sezioni principali: una 
    dedicata alle prestazioni complessive delle nazioni e l'altra focalizzata sulle edizioni specifiche. 
    Grazie alla flessibilità del pannello laterale, è possibile anche combinare i risultati di Germania Est e Ovest per un'analisi più completa. 
    </p>
    """,
    unsafe_allow_html = True
)

#dataframe per gli anni delle olimpiadi
years = medals.select("Year").unique().sort("Year").to_series().to_list()
df_years = pl.DataFrame({"Year": years})
noyears = [year for year in list(range(1896, 2025, 4))  if year not in years]
df_noyears = pl.DataFrame({"Year": noyears})
df_allyears = pl.concat([df_years, df_noyears]).sort("Year")

#lista delle nazioni
nations = medals.select("Nation").unique().sort("Nation").to_series().to_list()

#aggiunta colonna % medaglie d'oro
medals = medals.with_columns((pl.col("Gold") / pl.col("Total") * 100).alias("Gold%"))

#df aggregato per nazione
top_nations = (medals
              .group_by("Nation")
              .agg([pl.col("Gold").sum().alias("Gold"),
                    pl.col("Silver").sum().alias("Silver"),
                    pl.col("Bronze").sum().alias("Bronze"),
                    pl.col("Total").sum().alias("Total")]
              )
)

#tidy del df delle città
cities = cities.filter(~pl.col("Summer").is_null())
cities = cities.filter(pl.col("Year").is_in(years))
cities = cities.select(pl.col("City"), 
                       pl.col("Nation"), 
                       pl.col("Year"), 
                       pl.col("Region"), 
                       pl.col("Opening ceremony"), 
                       pl.col("Closing ceremony"))
#creazione nuove colonne con le date di apertura e chiusura dei giochi
cities = cities.with_columns(
    pl.col("Opening ceremony")
    .str.strptime(pl.Date, "%d %B %Y", strict = False)
    .alias("Opening date"),
    
    pl.col("Closing ceremony")
    .str.strptime(pl.Date, "%d %B %Y", strict = False)
    .alias("Closing date")   
)
#nuova colonna: durata in giorni dei giochi
cities = cities.with_columns(
    ((pl.col("Closing date") - pl.col("Opening date"))
     .cast(pl.Int64)/ (1000 * 60 * 60 * 24) + 1)
     .cast(pl.Int64)
     .alias("Days")
)

st.markdown("---")

#SEZIONE PER NAZIONE
st.markdown(
    """
    <div style="background-color: #f0f8ff; border-radius: 10px;">
    <h2> Analisi per Nazione </h2>
    </div>
    """,
    unsafe_allow_html = True
)

st.markdown("""<h3> 📊 Top 10 Nazioni per totale di medaglie </h3>""",
            unsafe_allow_html = True)

#ordino in base alla modalità scelta
option = st.selectbox("Seleziona un criterio per ordinare:", ["Totale", "Oro", "Argento", "Bronzo"])
sub_title = ""
if option == "Totale":
    criteria = ["Total", "Gold", "Silver", "Bronze"]
    sub_title = "Top **10** nazioni ordinate per n° **totale** di medaglie vinte"
elif option == "Oro":
    criteria = ["Gold", "Total", "Silver", "Bronze"]
    sub_title = "Top **10** nazioni ordinate per n° di **ori** vinti"
elif option == "Argento":
    criteria = ["Silver", "Gold", "Total", "Bronze"]
    sub_title = "Top **10** nazioni ordinate per n° di **argenti** vinti"
elif option == "Bronzo":
    criteria = ["Bronze", "Gold", "Silver", "Total"]
    sub_title = "Top **10** nazioni ordinate per n° di **bronzi** vinti"
top_nations = top_nations.sort(by = criteria, descending = [True] * 4)

#metto colonna rank all'inizio del df
col_rank = pl.Series("Rank", list(range(1, len(top_nations) + 1)))
top_nations = top_nations.insert_column(0, col_rank)

st.markdown(
    """
    <div class = "description">
    Questa tabella mostra il ranking delle nazioni che hanno dominato le competizioni olimpiche classificandole in base al numero totale di medaglie 
    vinte e ai vari metalli (oro, argento e bronzo). Utilizzando il menu a tendina è possibile ordinare le nazioni secondo il criterio che si preferisce.
    </div>
    """,
    unsafe_allow_html = True
)


#creo tabella great table
top_table = (
    GT(data = top_nations.head(10))
    .tab_header(
        title = md("Medagliere olimpico *Mondiale* &#x1F310;"),
        subtitle = md(sub_title)
    )
    .tab_spanner(label = "Nazione", columns = ["Rank","Nation"])
    .tab_spanner(label="Medaglie", columns = ["Gold", "Silver", "Bronze", "Total"])
    .tab_style(
        style.fill("yellow"),
        loc.body(  
            columns = cs.all(),
            rows = pl.col("Nation") == "Italy"
        )
    )
    .tab_style(
        style.text(align = "center"),
        loc.spanner_labels(["Medaglie"])
    )
    .tab_style(
        style.text(weight = "bold"),
        loc.column_labels(criteria[0])
    )
    .tab_style(
        style.text(align = "center"),
        loc.source_notes()
    )
    .tab_source_note(source_note = md("Fonte: [**Wikipedia**](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table) - Olympic Medal Counts by Country."))
    .as_raw_html()
)
st.html(top_table)

#descrizione
st.markdown(
    """
    <div class="description">
    Questi grafici a torta visualizzano la distribuzione percentuale delle medaglie d'oro, d'argento e di bronzo per le prime 10 nazioni nel ranking 
    olimpico. Ogni segmento dell'arco rappresenta la percentuale di ciascun tipo di medaglia, mentre il totale delle medaglie è visibile al centro di 
    ogni grafico, mentre i totali per ogni tipo di medaglia son riportati si lato ad ogni segmento
    </div>
    """,
    unsafe_allow_html = True
)


#creo grafici a torta delle top 10 nazioni
pie_data = (top_nations
            .head(10)
            .with_columns(
                (pl.col("Gold") / pl.col("Total") * 100).round(decimals = 2).cast(pl.Float64).alias("Gold_f"),
                (pl.col("Silver") / pl.col("Total") * 100).round(decimals = 2).cast(pl.Float64).alias("Silver_f"),
                (pl.col("Bronze") / pl.col("Total") * 100).round(decimals = 2).cast(pl.Float64).alias("Bronze_f")
            )
            .unpivot(
                index = "Nation",
                on = ["Gold_f", "Silver_f", "Bronze_f"],
                value_name = "Frac",
                variable_name = "Type"
            )
            .with_columns(
                pl.col("Type").str.replace("_f", "", literal = False),
            )
            .with_columns(
                pl.col("Frac").cast(pl.Float64)
            )
            .with_columns(
                pl.when(pl.col("Type") == "Gold").then(1)
                .when(pl.col("Type") == "Silver").then(2)
                .when(pl.col("Type") == "Bronze").then(3)
                .alias("Order")
            )                                   
)
base_data = (top_nations
             .unpivot(
                 index = "Nation",
                 on = ["Gold", "Silver", "Bronze"],
                 value_name = "Count",
                 variable_name = "Type"
             )
             .with_columns(
                 pl.col("Count").cast(pl.Int64)
             )
)   
pie_data = (pie_data
            .join(base_data,
                  on = ["Nation", "Type"],
                  how = "left"
            )
            .join(top_nations.select(pl.col("Nation"), pl.col("Total")), 
                  on = ["Nation"], 
                  how = "left"
            )
)

base_pie = alt.Chart(pie_data)
pie_chart = (base_pie
             .mark_arc(radius = 45, radius2 = 65, cornerRadius = 10)
             .encode(
                 alt.Theta("Frac"),
                 alt.Color(
                     "Type", 
                     scale = alt.Scale(domain = ["Gold", "Silver", "Bronze"], range = ["#FFD700", "#C0C0C0", "#CD7F32"]),
                     legend = alt.Legend(orient = "top", title = None)
                 ),
                 alt.Order("Order", sort = "ascending"),
                 tooltip = [                   
                     alt.Tooltip("Type", title = "Tipologia"),
                     alt.Tooltip("Frac", title = "%"),
                 ]
             )
             .properties(width = 175, height = 220)
)
text_chart = (base_pie
              .mark_text(radius = 80)
              .encode(
                  alt.Theta("Frac", stack = True),
                  alt.Text("Count"),
                  alt.Order("Order", sort = "ascending")
              )
)
big_text_chart = (alt.Chart(pie_data)
                  .mark_text(size = 20, radius = 0)
                  .encode(alt.Text("Total"))
)

st.altair_chart((pie_chart + text_chart + big_text_chart)
                .facet(
                    alt.Row("Nation", title = None, sort = alt.EncodingSortField(field = "Rank", order = "ascending")), 
                    columns = 4, 
                    spacing = 5, 
                    bounds = "flush"
                )
                .properties(title = "Distribuzione delle medaglie delle top 10 nazioni")
                .configure_title(anchor = "middle")
)



st.markdown("""<h3> ⏳ Serie temporale delle medaglie </h3>""",
            unsafe_allow_html = True)
selected_nations = st.multiselect(
    "Seleziona uno o più stati",
    nations,
    max_selections = 4,
    default = "Italy"
)

#descrizione
st.markdown(
    """
    <div class = "description">
    Questo grafico mostra l'evoluzione nel tempo delle medaglie vinte dagli stati selezionati. Le barre rosse indicano gli anni in cui le Olimpiadi non 
    si sono svolte a causa delle due guerre mondiali (1916, 1940 e 1944). Utilizzando il filtro in alto, è possibile scegliere fino a 
    quattro stati da confrontare tra loro. Il limite di quattro stati è stato imposto esclusivamente per mantenere il grafico leggibile e non 
    sovraccaricarlo di dati.
    </div>
    """,
    unsafe_allow_html = True
)

#selezione delle nazioni e aggregazione per anno
ts_data = (medals
           .filter(pl.col("Nation").is_in(selected_nations))
           .group_by(["Year", "Nation"])
           .agg([
               pl.col("Gold").sum().alias("Gold"),
               pl.col("Silver").sum().alias("Silver"),
               pl.col("Bronze").sum().alias("Bronze"),
               pl.col("Total").sum().alias("Total")
           ])
)
#creo serie temporale
empty_chart = (
    alt.Chart(df_allyears)
    .mark_line(opacity=0) 
    .encode(alt.X("Year:O", title = "Anno"))
)
line_chart = (
    alt.Chart(ts_data)
    .mark_line()
    .encode(
        alt.X("Year:O", title = "Anno", axis = alt.Axis(values = years)),
        alt.Y("Total:Q", title = "Totale medaglie"),
        alt.Color(
            "Nation:N", 
            scale = alt.Scale(scheme = "viridis"), 
            title = "Nazione"
        )
    )
)
point_chart = (
    alt.Chart(ts_data)
    .mark_point(size = 50)
    .encode(
        alt.X("Year:O", title = "Anno", axis = alt.Axis(values = years)),
        alt.Y("Total:Q"),
        alt.Color("Nation:N", title = "Nazione"),
        tooltip = [
            alt.Tooltip("Nation:N", title = "Nazione"),
            alt.Tooltip("Year:O", title = "Anno"),
            alt.Tooltip("Gold:Q", title = "Ori"),
            alt.Tooltip("Silver:Q", title = "Argenti"),
            alt.Tooltip("Bronze:Q", title = "Bronzi"),
            alt.Tooltip("Total:Q", title = "Totale")
        ]
    )
)
#aggiungo anni in cui non sono avvenute le olimpiadi
year_chart = (
    alt.Chart(df_noyears)
    .mark_rect(opacity = 0.4, color = "red") 
    .encode(alt.X("Year:O"))
)

st.altair_chart(
    (empty_chart + line_chart + point_chart + year_chart)
    .properties(title = f"Serie Temporale delle Medaglie - {', '.join(selected_nations)}")
    .configure_title(anchor = "middle"),
    use_container_width = True
)



st.markdown("""<h3> 📈 Relazione tra medaglie ed edizioni </h3>""",
            unsafe_allow_html = True)

#descrizione
st.markdown(
    """
    <div class = "description">
    Il grafico rappresenta la relazione tra il totale delle medaglie vinte e il numero di edizioni olimpiche a cui ciascuna nazione ha vinto alemno 
    una medaglia. Il colore dei punti è proporzionale al totale delle medaglie vinte (in scala logaritmica). Si nota una relazione di tipo lineare tra
    le due variabili, per questo motivo si è deciso di aggiungere una linea rossa la quale rappresenta il modello di regressione esponenziale calcolato 
    attravero i dati 
    </div>
    """,
    unsafe_allow_html = True
)

#aggiungo il numero di edizioni olimpiche partecipate al df
nation_editions = (medals
                   .group_by("Nation")
                   .agg([pl.col("Year").n_unique().alias("Ol_ed")])
)
top_nations = top_nations.join(nation_editions, on = "Nation")
#trasformo in logartimo
top_nations = top_nations.with_columns(
    (pl.col("Total").log()).alias("Log_Total")
)
#creo modello lineare
x = top_nations["Ol_ed"].to_numpy()
y = top_nations["Log_Total"].to_numpy()
x = sm.add_constant(x)
model = sm.OLS(y, x).fit()
a = np.exp(model.params[0])
b = model.params[1]
#aggiungo valori predetti al df
top_nations = top_nations.with_columns((a * np.exp(b * pl.col("Ol_ed"))).alias("Predicted"))

#creo grafico
point_chart = (alt.Chart(top_nations)
          .mark_circle(size = 100, stroke = "black", strokeWidth = 0.5)
          .encode(
              alt.X("Ol_ed:Q", title = "Numero di edizioni olimpiche"),
              alt.Y("Total:Q", scale = alt.Scale(type = "log"), title = "Totale medaglie"),
              alt.Color("Total:Q", title = "Totale medaglie").scale(scheme = "viridis"),
              tooltip=[
                  alt.Tooltip("Nation:N", title = "Nazione"),
                  alt.Tooltip("Total:Q", title = "Totale"),
                  alt.Tooltip("Ol_ed:Q", title = "Numero edizioni")
              ]
          )
)
regr_line = (alt.Chart(top_nations)
             .mark_line(color = "red", size = 2)
             .encode(
                 alt.X("Ol_ed:Q"),
                 alt.Y("Predicted:Q")
             )
)

st.altair_chart((point_chart + regr_line)
                .properties(title = "Relazione tra numero di medaglie e numero di edizioni olimpiche per nazione")
                .configure_title(anchor = "middle"),
                use_container_width = True)

#commento
st.markdown(
    """
    <div class = "description-top">
    Dopo aver analizzato la distribuzione delle medaglie, si evince che esiste un forte effetto di tipo esponenziale tra il numero di edizioni olimpiche 
    e il numero di medaglie. Questo significa che con l'aumento delle edizioni olimpiche si osserva un incremento esponenziale del totale delle medaglie.
    Il modello di regressione mostra una chiara relazione esponenziale, confermata dai dati. 
    Di seguito è mostrato il modello esponenziale che rappresenta questa relazione:
    </div>
    """,
    unsafe_allow_html = True
)
st.latex(r'''y = a \cdot e^{b \cdot x}''')
st.markdown(
    f"""
    <div class = "description-bottom">
    Il modello esponenziale sopra riportato si basa sull'analisi statistica dei dati e può essere interpretato come segue:
    y è il numero previsto di medaglie totali, x è il numero di edizioni olimpiche, a è il fattore moltiplicativo e vale {a:.2f}, mentre b è il 
    coefficiente di crescita esponenziale della relazione esponenziale e vale {b:.2f}.
    </div>
    """,
    unsafe_allow_html = True
)

st.markdown("---")

#SEZIONE PER EDIZIONE
st.markdown(
    """
    <div style = "background-color: #f0f8ff; border-radius: 10px;">
    <h2> Analisi per Edizione </h2>
    </div>
    """,
    unsafe_allow_html = True
)

st.markdown("""<h3> 📊 Top 10 Nazioni per totale di medaglie per edizione </h3>""",
            unsafe_allow_html = True)

year = st.selectbox("Seleziona l'anno:", years)

#descrizione
st.markdown(
    """
    <div class = "description">
    Il grafico mostra le prime 10 nazioni per numero totale di medaglie nell'anno selezionato (utilizza la barra in alto per selezionare un anno). 
    Le barre rappresentano il numero totale di medaglie vinte da ciascuna nazione, mentre il colore delle barre riflette la percentuale di medaglie 
    d'oro rispetto al totale delle medaglie vinte dalla nazione stessa.
    </div>
    """,
    unsafe_allow_html = True
)

#df filtrato per anno selezionato
top_10year = (medals
              .filter(pl.col("Year") == year)
              .sort("Total", descending = True).head(10)
)

#creo grafico
chart = (
    alt.Chart(top_10year)
    .mark_bar()
    .encode(
        alt.X("Nation:N", sort = "-y", title = "Nazione"),
        alt.Y("Total:Q", title = "Totale medaglie"),
        alt.Color("Gold%:Q", 
                  title = "% Medaglie d'Oro", 
                  scale = alt.Scale(scheme = "goldorange", domain = [0, 100])),
        tooltip = [
            alt.Tooltip("Nation:N", title = "Nazione"),
            alt.Tooltip("Gold:Q", title = "Ori"),
            alt.Tooltip("Silver:Q", title = "Argenti"),
            alt.Tooltip("Bronze:Q", title = "Bronzi"),
            alt.Tooltip("Total:Q", title = "Totale")
        ])
)

st.altair_chart(chart, 
                use_container_width = True)



st.markdown("""<h3> 📈 Evoluzione delle medaglie assegnate </h3>""", 
            unsafe_allow_html = True)

#descrizione
st.markdown(
    """
    <div class = "description">
    Il grafico mostra l'evoluzione nel tempo del totale delle medaglie assegnate nelle Olimpiadi. La linea indicana l'andamento delle medaglie totali, 
    mentre i punti evidenziano i valori per ciascun anno. Si osserva un trend crescente nel numero di medaglie assegnate, con un aumento particolarmente 
    significativo dagli anni '60 fino ai primi anni 2000. Tuttavia è importante notare che alcune medaglie assegnate a delegazioni olimpiche 
    non riconducibili a una nazione sono state rimosse dal dataset iniziale. Nonostante ciò, queste medaglie non hanno un impatto significativo 
    sull'andamento del grafico.
    </div>
    """,
    unsafe_allow_html = True
)

#df del totale delle medaglie per ogni anno
medals_years = (
    medals
    .group_by("Year")
    .agg([
        pl.col("Gold").sum().alias("Gold"),
        pl.col("Silver").sum().alias("Silver"),
        pl.col("Bronze").sum().alias("Bronze"),
        pl.col("Total").sum().alias("Total")
        ])
)

#creo grafico
line_chart = (
    alt.Chart(medals_years)
    .mark_line()
    .encode(
        alt.X("Year:O", title = "Anno"),
        alt.Y("Total:Q", title = "Totale Medaglie")
    )

)
point_chart = (
    alt.Chart(medals_years)
    .mark_point(size = 50)
    .encode(
        alt.X("Year:O"),
        alt.Y("Total:Q"),
        tooltip = [
            alt.Tooltip("Year:O", title = "Anno"),
            alt.Tooltip("Gold:Q", title = "Ori"),
            alt.Tooltip("Silver:Q", title = "Argenti"),
            alt.Tooltip("Bronze:Q", title = "Bronzi"),
            alt.Tooltip("Total:Q", title = "Totale medaglie")
        ]
    )
)

st.altair_chart((line_chart + point_chart + year_chart)
                .properties(title="Evoluzione delle Medaglie Totali Assegnate")
                .configure_title(anchor = "middle"), 
                use_container_width = True)



st.markdown("""<h3> 🍰 Distribuzione delle edinizioni olimpiche per continente </h3>""", 
            unsafe_allow_html = True)

#descrizione
st.markdown(
    """
    <div class = "description">
    Il grafico mostra la distribuzione delle Olimpiadi per continente. Ogni arco della torta corrisponde a un continente e la sua grandezza è 
    proporzionale al numero di edizioni olimpiche ospitate da ciascun continente. Dal grafico si può osservare una netta predominanza di alcuni 
    continenti in termini di edizioni olimpiche ospitate con un focus particolare sull'Europa e l'America del Nord che insieme hanno ospitato i tre
    quarti delle Olimpiadi nel corso della storia.
    </div>
    """,
    unsafe_allow_html = True
)

#df edizioni raggruppate per continente
region_data = (
    cities
    .group_by("Region")
    .agg(pl.col("Year").count().alias("Count"))
    .sort("Count", descending = True)
)

#creo grafico
pie_chart = (
    alt.Chart(region_data)
    .mark_arc(radius = 70, radius2 = 100, cornerRadius = 10)
    .encode(
        alt.Theta("Count:Q", title = "Numero di edizioni"),
        alt.Color("Region:N", title = "Contiente", scale = alt.Scale(scheme = "category10")),
        alt.Order("Count:Q", sort = "descending"),
        tooltip = [
            alt.Tooltip("Region:N", title = "Contiente"),
            alt.Tooltip("Count:Q", title = "Numero di edizioni")
        ]
    )
    
)
big_text_chart = (alt.Chart(pl.DataFrame({"Count" : region_data["Count"].sum()}))
                  .mark_text(size = 70, radius = 0)
                  .encode(alt.Text("Count"))
)

st.altair_chart((pie_chart + big_text_chart)
                .properties(title = "Distribuzione delle Olimpiadi per continente")
                .configure_title(anchor = "middle"), 
                use_container_width = True)


hosting_cities = (
    cities
    .group_by("Nation")
    .agg(pl.col("Year").count().alias("Edizioni Ospitate"))
    .sort("Edizioni Ospitate", descending=True)
)

#st.dataframe(hosting_cities)

st.markdown("""<h3> 🔍 Prestazioni olimpiche dei paesi ospitanti </h3>""", 
            unsafe_allow_html = True)

#descrizione
st.markdown(
    """
    <div class = "description">
    Il grafico mostra le prestazioni olimpiche dei paesi che nel corso della storia hanno ospitato almeno un'edizione dei giochi. Per ragioni di spazio
    e per migliorare la chiarezza visiva, i box-plot sono stati suddivisi in due gruppi. Ogni box-plot rappresenta la distribuzione delle medaglie 
    olimpiche totali di un paese, mentre i punti di colore ciano indicano i dati specifici del paese nell'anno o negli anni in cui ha ospitato i giochi.
    L'obiettivo di questo grafico è capire se ospitare un'Olimpiade abbia un impatto positivo sulle performance olimpiche del paese ospitante.
    </div>
    """,
    unsafe_allow_html = True
)

#df medaglie paesi opspitanti (tutti gli anni)
host_nations = cities.select("Nation").unique().sort("Nation").to_series().to_list()
all_continents = cities.select("Region").unique().to_series().to_list()
#divido a metà per convenzione
half = len(host_nations) // 2
g1 = host_nations[:half]
g2 = host_nations[half:]
g1_medals = (
    medals
    .filter(pl.col("Nation").is_in(g1))
    .join(cities.select(["Nation", "Region"]),
          on = "Nation",
          how = "left")
)
g2_medals = (
    medals
    .filter(pl.col("Nation").is_in(g2))
    .join(cities.select(["Nation", "Region"]),
          on = "Nation",
          how = "left")
)
#performance olimpiche dei paesi mentre ospitavano
host_perf = (
    medals
    .join(cities,
        on = ["Year", "Nation"],
        how = "left")
    .filter(~pl.col("City").is_null())
)
host_perf1 = host_perf.filter(pl.col("Nation").is_in(g1))
host_perf2 = host_perf.filter(pl.col("Nation").is_in(g2))

#creo i due boxplot
boxplot1 = (
    alt.Chart(g1_medals)
    .mark_boxplot(size = 45)
    .encode(
        alt.X("Nation:N"),  
        alt.Y("Total:Q", title = "Totale medaglie", scale = alt.Scale(domain = [0, 240])),
        alt.Color(
            "Region:N",
            title = "Continente",
            scale = alt.Scale(scheme = "category10"), 
            legend = alt.Legend(orient = "top", titleAnchor = "middle") 
        )
    )
)
boxplot2 = (
    alt.Chart(g2_medals)
    .mark_boxplot(size = 45)
    .encode(
        alt.X("Nation:N"),  
        alt.Y("Total:Q", title="Totale medaglie", scale = alt.Scale(domain = [0, 240])),
        alt.Color("Region:N", title = "Contiente", legend = None)
    )
)
point_chart1 = (
    alt.Chart(host_perf1)
    .mark_point(shape = "circle", size = 100, filled = True, color = "cyan")
    .encode(
        alt.X("Nation:N"),
        alt.Y("Total:Q"),
        tooltip = [
            alt.Tooltip("Nation:N", title = "Nazione"),
            alt.Tooltip("Year:O", title = "Anno"),
            alt.Tooltip("Gold:Q", title = "Ori"),
            alt.Tooltip("Silver:Q", title = "Argenti"),
            alt.Tooltip("Bronze:Q", title = "Bronzi"),
            alt.Tooltip("Total:Q", title = "Totale")
        ]
    )
)
point_chart2 = (
    alt.Chart(host_perf2)
    .mark_point(shape = "circle", size = 100, filled = True, color = "cyan")
    .encode(
        alt.X("Nation:N"),
        alt.Y("Total:Q"),
        tooltip = [
            alt.Tooltip("Nation:N", title = "Nazione"),
            alt.Tooltip("Year:O", title = "Anno"),
            alt.Tooltip("Gold:Q", title = "Ori"),
            alt.Tooltip("Silver:Q", title = "Argenti"),
            alt.Tooltip("Bronze:Q", title = "Bronzi"),
            alt.Tooltip("Total:Q", title = "Totale")
        ]
    )
)
final_chart = (
    alt.vconcat((boxplot1 + point_chart1), (boxplot2 + point_chart2))
    .resolve_scale(color = "shared")
)

st.altair_chart(final_chart,
                use_container_width = True)

#commento
st.markdown(
    """
    <div class = "description">
    Dal grafico si evince che la maggior parte dei punti color ciano si trovano nella parte alta dei boxplot indicando quindi un trend positivo: 
    ospitare le Olimpiadi sembra avere un impatto positivo sul numero di medaglie vinte. Tuttavia ci sono delle eccezioni come la Finlandia, i Paesi Bassi
    e il Canada dove le prestazioni non sono migliorate significativamente durante gli anni in cui hanno ospitato i giochi. Nonostante queste eccezioni, 
    l'andamento generale suggerisce che ospitare le Olimpiadi possa avere un'influenza positiva sul paese ospitante in termini di medaglie.
    </div>
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