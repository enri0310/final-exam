import streamlit as st
import polars as pl
import altair as alt
import utils as utl

utl.setup_page(
    title = "Europa",
    icon = "🇪🇺",
    layout = "centered",
    css_file = "styles.css"
)

st.title("Analisi delle Medaglie Olimpiche in Unione Europea")

medals = st.session_state.medal
europe = st.session_state.europe

renamed = {"East Germany": "Germany", 
           "West Germany": "Germany"}


medals_renamed = medals.with_columns(
    pl.when(pl.col("Nation") == "East Germany")
    .then(pl.lit("Germany")).when(pl.col("Nation") == "West Germany")
    .then(pl.lit("Germany"))
    .alias("Germany")
)

medals_with_europe = medals_renamed.join(
    europe.rename({"Year": "eu_Year"}), 
    on="Nation", 
    how="left"  
)
eu_medals = (medals_renamed
          .join(
              europe.rename({"Year": "eu_Year"}), 
              on="Nation", 
              how="left"
          )
          .with_columns(
              pl.when(pl.col("Year") < pl.col("eu_Year"))
              .then(None)
              .otherwise(pl.col("Year"))
              .alias("Year")
          )
          .filter(pl.col("Nation").is_in(europe.select("Nation").unique().to_series().to_list()))
          .filter(pl.col("Year").is_not_null())
)
eu_medals

medal_counts = eu_medals.group_by("Nation").agg([pl.col("Gold").sum().alias("Gold"),
                    pl.col("Silver").sum().alias("Silver"),
                    pl.col("Bronze").sum().alias("Bronze"),
                    pl.col("Total").sum().alias("Total Medals")]).sort("Total Medals", descending= True)

bar_chart = (
    alt.Chart(medal_counts)
    .mark_bar()
    .encode(
        alt.X("Nation:N", sort = "-y"),
        alt.Y("Total Medals:Q"),
        alt.Color("Nation:N"),
        alt.Tooltip(["Nation", "Total Medals"])
    )
    .properties(title="Totale Medaglie Olimpiche per Paese dell'UE")
)

st.altair_chart(bar_chart, 
                use_container_width = True)

medal_counts
top_14 = medal_counts[:14]
other_nations = medal_counts[14:]
st.metric(
    label="Nazioni Partecipanti",
    value=None
)
st.metric(
    label="Nazioni Vincitrici",
    value=None
)
# Calcola il totale per le altre nazioni
other_total = other_nations.select(pl.col("Total Medals").sum()).item()
other_row = {"Nation": "Altre", "Gold": 0, "Silver": 0, "Bronze": 0, "Total Medals": other_total}

# Combina le prime 14 nazioni con "Altre"
final_data = pl.DataFrame(top_14.vstack(pl.DataFrame([other_row])))

# Crea il grafico a torta
pie_chart = alt.Chart(final_data).mark_arc().encode(
    theta=alt.Theta("Total Medals:Q"),
    color=alt.Color("Nation:N", legend=alt.Legend(title="Nazione")),
    tooltip=["Nation", "Total Medals"]
).properties(
    title="Distribuzione delle Medaglie Olimpiche per Nazione dell'UE"
)

# Mostra il grafico in Streamlit
st.altair_chart(pie_chart, use_container_width=True)

stacked_pie_chart = alt.Chart(eu_medals).mark_arc().encode(
    theta=alt.Theta("value:Q", title="Numero di Medaglie"),
    color=alt.Color("Nation:N", legend=alt.Legend(title="Nazione")),
    tooltip=["Nation", "variable:N", "value:Q"]
).facet(
    column=alt.Column("variable:N", header=alt.Header(title="Tipo di Medaglia"))
).transform_fold(
    ["Gold", "Silver", "Bronze"],  # Specifica le colonne da trasformare
    as_=["variable", "value"]  # Nomina le nuove colonne create
).properties(
    title="Distribuzione delle Medaglie per Tipo"
)

# Visualizzare il grafico in Streamlit
st.altair_chart(stacked_pie_chart)

