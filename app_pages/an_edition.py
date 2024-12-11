import streamlit as st
import polars as pl
import altair as alt
import numpy as np
import utils as utl

utl.setup_page(
    title="Edizioni",
    icon="🏅",
    layout="centered",
    css_file="styles.css"
)

st.title("Analisi delle Medaglie Olimpiche per Edizione")

medals = st.session_state.medal

st.markdown("""<h3> 📊 Top 10 Nazioni per Totale di Medaglie </h3>""",
            unsafe_allow_html = True)
year = st.selectbox("Seleziona l'anno:", medals['Year'].unique())
data = medals.filter(pl.col("Year") == year)
data = data.with_columns(pl.col("Total").cast(pl.Int64))
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

st.altair_chart(chart, 
                use_container_width=True)


pie_data = (
    data
    .with_columns(
        (pl.col("Gold") / pl.col("Total") * 100).alias("Gold_pct"),
        (pl.col("Silver") / pl.col("Total") * 100).alias("Silver_pct"),
        (pl.col("Bronze") / pl.col("Total") * 100).alias("Bronze_pct")
    )
    .unpivot(
        index="Nation",
        on =["Gold_pct", "Silver_pct", "Bronze_pct"],
        variable_name="Medal Type",
        value_name="Percentage"
    )
)
pie_data
pie_chart = (
    alt.Chart(pie_data)
    .mark_arc()
    .encode(
        alt.Theta("Percentage:Q", title="Percentuale"),
        alt.Color("Medal Type:N", scale=alt.Scale(scheme="category20b")),
        alt.Tooltip(["Nation", "Medal Type", "Percentage"])
    )
    .properties(title=f"Distribuzione delle Medaglie - {year}")
)

st.altair_chart(pie_chart, use_container_width=True)



total_nations = medals.filter(pl.col("Year") == year)["Nation"].n_unique()
winning_nations = data["Nation"].n_unique()

st.metric(
    label="Nazioni Partecipanti",
    value=total_nations
)
st.metric(
    label="Nazioni Vincitrici",
    value=winning_nations
)

medals_by_year = (
    medals
    .group_by("Year")
    .agg(pl.col("Total").sum().alias("Total Medals"))
    .sort("Year")
)

line_chart = (
    alt.Chart(medals_by_year)
    .mark_line()
    .encode(
        alt.X("Year:O", title="Anno"),
        alt.Y("Total Medals:Q", title="Totale Medaglie"),
        alt.Tooltip(["Year", "Total Medals"])
    )
    .properties(title="Evoluzione delle Medaglie Totali Assegnate")
)

st.altair_chart(line_chart, use_container_width=True)

cities = st.session_state.city  # Dati delle edizioni
cities
# Calcolo della durata delle Olimpiadi
cities = cities.with_columns(
    [
        pl.col("Opening ceremony")
        .str.strptime(pl.Date, "%d %B %Y", strict=False)
        .alias("Opening date"),
        
        pl.col("Closing ceremony")
        .str.strptime(pl.Date, "%d %B %Y", strict=False)
        .alias("Closing date")
    ]
)
cities = cities.with_columns(
    [
        pl.col("Opening ceremony")
        .str.strptime(pl.Date, "%d %B %Y", strict=False)
        .alias("Opening date"),
        
        pl.col("Closing ceremony")
        .str.strptime(pl.Date, "%d %B %Y", strict=False)
        .alias("Closing date")
    ]
)

# Correzione del calcolo della durata in giorni
cities = cities.with_columns(
    (
        (pl.col("Closing date") - pl.col("Opening date"))
        .cast(pl.Int64)  # La durata viene data in nanosecondi
        .alias("Duration (ns)")  # Aggiungiamo una colonna per la durata in nanosecondi
    )
)

# Ora, convertiamo i nanosecondi in giorni (1 giorno = 86400 secondi = 86400000000000 nanosecondi)
cities = cities.with_columns(
    (
        (pl.col("Duration (ns)") / 86400000000000).cast(pl.Int64())  # Conversione in giorni
    ).alias("Duration (days)")
)

# Filtrare le edizioni dopo la Seconda Guerra Mondiale (1945 in poi)
cities_post_ww2 = cities.filter(pl.col("Year") >= 1945)

# Stampa delle righe con le date non valide per il debug
invalid_rows = cities.filter(pl.col("Opening date").is_null() | pl.col("Closing date").is_null())
print(invalid_rows)

# Visualizzazione del grafico con i dati filtrati
import altair as alt

chart = alt.Chart(cities_post_ww2).mark_bar().encode(
    x='Year:O',
    y='Duration (days):Q',
    color='City:N',
).properties(title="Durata delle edizioni Olimpiche (dopo la Seconda Guerra Mondiale)")

chart.show()

# Calcolo della durata solo per righe valide (entrambe le date non sono null)
cities = cities.with_columns(
    (
        (pl.col("Closing date") - pl.col("Opening date"))
        .cast(pl.Int64)  # Converte la durata in giorni come intero
    ).alias("Duration (days)")
)
# Somma delle medaglie per anno
total_medals_by_year = (
    medals.group_by("Year")
    .agg(pl.col("Total").sum().alias("Total Medals"))
)

# Merge dei dati
analysis_data = cities.join(total_medals_by_year, on="Year", how="inner")

# Grafico: Durata vs Medaglie Totali
chart = (
    alt.Chart(analysis_data)
    .mark_circle(size=100, opacity=0.8)
    .encode(
        alt.X("Duration (days):Q", title="Durata (giorni)"),
        alt.Y("Total Medals:Q", title="Totale Medaglie Assegnate"),
        alt.Color("Region:N", title="Regione"),
        tooltip=["Year", "City", "Country", "Duration (days)", "Total Medals"]
    )
    .properties(
        title="Relazione tra Durata delle Olimpiadi e Medaglie Totali Assegnate",
        width=700,
        height=400
    )
)

st.altair_chart(chart, use_container_width=True)

# Analisi aggiuntiva: Mostra i dettagli di ogni edizione
st.markdown("### Dettagli delle Edizioni")
st.dataframe(analysis_data)