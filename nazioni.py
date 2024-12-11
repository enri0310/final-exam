import streamlit as st
import polars as pl
import altair as alt
import numpy as np
import utils as utl

utl.setup_page(
    title="Nazioni",
    icon="🏅",
    layout="centered",
    css_file="styles.css"
)

st.title("Analisi delle Medaglie Olimpiche per Nazione")

medals = st.session_state.medal
renamed = {}

# Widget per decisioni interattive
czechoslovakia_choice = st.selectbox(
    "Come gestire 'Czechoslovakia'?",
    ["Czechoslovakia", "Czech Republic", "Slovakia"]
)

# 2. Gestione Soviet Union
soviet_choice = st.selectbox(
    "Come gestire 'Soviet Union'?",
    ["Soviet Union",
    "Russia", 
    "Ukraine",
    "Belarus",
    "Estonia",
    "Latvia",
    "Lithuania",
    "Moldova",
    "Georgia",
    "Armenia",
    "Azerbaijan",
    "Kazakhstan",
    "Uzbekistan",
    "Turkmenistan",
    "Kyrgyzstan",
    "Tajikistan"]
)

# 3. Gestione East Germany e West Germany
germany_choice = st.selectbox(
    "Come gestire 'East Germany' e 'West Germany'?",
    ["Germania unificata", "Mantienili separati"]
)

# 4. Gestione Yugoslavia
yugoslavia_choice = st.selectbox(
    "Come gestire 'Yugoslavia'?",
    ["Yugoslavia", "Slovenia", "Croatia", "Bosnia and Herzegovina", "Serbia", "Montenegro", "North Macedonia", "Kosovo"]
)

renamed["Czechoslovakia"] = czechoslovakia_choice
renamed["Soviet Union"] = soviet_choice

if germany_choice == "Germania unificata":
    renamed["East Germany"] = "Germany"
    renamed["West Germany"] = "Germany"

renamed["Yugoslavia"] = yugoslavia_choice

medals = medals.with_columns(
    pl.col("Nation").map_elements(lambda x: renamed.get(x, x)).alias("newNation")
)


year = st.selectbox("Seleziona l'anno:", medals['Year'].unique())

data = medals.filter(pl.col("Year") == year)

# Assicurati che 'Total' sia numerico
data = data.with_columns(pl.col("Total").cast(pl.Int64))

# Ordina in ordine decrescente per 'Total' e seleziona i primi 10
data = data.sort("Total", descending=True).head(10)


chart = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        alt.X("Nation", sort="-y", title="Nazione"),
        alt.Y("Total", title="Totale Medaglie"),
        alt.Color("Gold", title="Medaglie d'Oro", scale=alt.Scale(scheme="oranges")),
        alt.Tooltip([
            "Nation", "Gold", "Silver", "Bronze", "Total"
        ])
    )
)

# Mostra il grafico su Streamlit
st.altair_chart(chart, 
                use_container_width=True)
# Sidebar per scegliere il numero di nazioni da visualizzare
top_n = st.sidebar.slider("Numero di nazioni da visualizzare:", min_value=1, max_value=50, value=10)

# Widget per selezionare l'anno
available_years = medals.select("Year").unique().to_series().sort().to_list()
selected_year = st.selectbox("Seleziona un anno:", available_years)

# --- Primo Grafico: Top N Nazioni per Totale Medaglie ---
st.markdown("## 📊 Top N Nazioni per Totale Medaglie")

# Filtraggio dei dati per anno
filtered_data = medals.filter(pl.col("Year") == selected_year)

# Aggregazione dei dati per conteggiare le medaglie
medals_count = (
    filtered_data.group_by("Nation")
    .agg(
        [
            pl.col("Gold").sum().alias("Gold"),
            pl.col("Silver").sum().alias("Silver"),
            pl.col("Bronze").sum().alias("Bronze"),
            pl.col("Total").sum().alias("Total"),
        ]
    )
    .sort("Total", descending=True)
)

# Selezionare le prime "top_n" nazioni
top_n_medals = medals_count.head(top_n)

# Conversione al formato pandas per Altair
top_n_medals_pd = top_n_medals.to_pandas()

# Creazione del grafico con Altair
chart = (
    alt.Chart(top_n_medals_pd)
    .mark_bar()
    .encode(
        x=alt.X("Nation:N", title="Nazione", sort="-y"),
        y=alt.Y("Total:Q", title="Numero Totale di Medaglie"),
        color=alt.Color("Nation:N", legend=None),
        tooltip=["Nation", "Gold", "Silver", "Bronze", "Total"],
    )
    .properties(
        width=800,
        height=400,
        title=f"Top {top_n} Nazioni per Totale Medaglie - {selected_year}",
    )
)

# Visualizzazione del primo grafico
st.altair_chart(chart, use_container_width=True)

# --- Secondo Grafico: Serie Temporale ---
st.markdown("## 📈 Serie Temporale delle Medaglie per Nazione")

# Widget per selezionare una nazione
unique_nations = medals.select("Nation").unique().to_series().sort().to_list()
selected_nation = st.selectbox("Seleziona una nazione:", unique_nations)

# Intervallo di anni completo
all_years = pl.DataFrame({"Year": available_years})

# Filtraggio dei dati per la nazione selezionata
nation_data = medals.filter(pl.col("Nation") == selected_nation)

# Aggregazione dei dati per anno
time_series_data = (
    nation_data.group_by("Year")
    .agg(
        [
            pl.col("Gold").sum().alias("Gold"),
            pl.col("Silver").sum().alias("Silver"),
            pl.col("Bronze").sum().alias("Bronze"),
            pl.col("Total").sum().alias("Total"),
        ]
    )
)

# Unione con tutti gli anni (aggiunge righe mancanti con valori null)
time_series_data = all_years.join(time_series_data, on="Year", how="left").fill_null(0)

# Conversione al formato pandas per Altair
time_series_data_pd = time_series_data.to_pandas()

# Aggiungi una colonna per distinguere anni senza dati
time_series_data_pd["LineStyle"] = np.where(
    time_series_data_pd["Total"] == 0, "dashed", "solid"
)

# Creazione del grafico della serie temporale con linea interrotta
time_series_chart = (
    alt.Chart(time_series_data_pd)
    .mark_line(point=True)
    .encode(
        x=alt.X("Year:O", title="Anno"),
        y=alt.Y("Total:Q", title="Totale Medaglie"),
        color=alt.value("#1f77b4"),
        strokeDash=alt.StrokeDash("LineStyle:N", legend=None),  # Linea interrotta
        tooltip=["Year", "Gold", "Silver", "Bronze", "Total"],
    )
    .properties(
        width=800,
        height=400,
        title=f"Serie Temporale delle Medaglie - {selected_nation}",
    )
)

# Visualizzazione del grafico
st.altair_chart(time_series_chart, use_container_width=True)


data = {
    "Nazione": ["USA", "URSS", "Germania"],
    "Oro": [1180, 473, 293],
    "Argento": [957, 376, 293],
    "Bronzo": [841, 355, 323],
    "Totale": [2978, 1204, 909]
}
df = pl.DataFrame(data)

# Selettore dinamico
opzione = st.selectbox("Seleziona un criterio per ordinare:", ["Totale", "Oro", "Argento", "Bronzo"])
#df_sorted = df.sort(by=opzione, ascending=False)
df_sorted = df.sort(by = opzione, descending = True)


st.table(df_sorted)