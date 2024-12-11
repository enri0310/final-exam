import streamlit as st
import altair as alt
import polars as pl

medals = st.session_state.medal
st.title("Medagliere Storico 🥇🥈🥉")
st.write("Esplora il medagliere per anno e nazione:")

# Seleziona l'anno
st.markdown("""<h3> 📊 Top 10 Nazioni per Totale di Medaglie </h3>""",
            unsafe_allow_html = True)
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




pie_data = (
    data
    .with_columns(
        (pl.col("Gold") / pl.col("Total") * 100).alias("Gold_pct"),
        (pl.col("Silver") / pl.col("Total") * 100).alias("Silver_pct"),
        (pl.col("Bronze") / pl.col("Total") * 100).alias("Bronze_pct")
    )
    .unpivot(
        index="Nation",
        value_vars=["Gold_pct", "Silver_pct", "Bronze_pct"],
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

cities = st.session_state.cities  # Dati delle edizioni

# Calcolo della durata delle Olimpiadi
cities = cities.with_columns(
    (
        (pl.col("Closing ceremony").str.strptime(pl.Date, "%Y-%m-%d") - 
         pl.col("Opening ceremony").str.strptime(pl.Date, "%Y-%m-%d")).dt.days
    ).alias("Duration (days)")
)

# Somma delle medaglie per anno
total_medals_by_year = (
    medals.groupby("Year")
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