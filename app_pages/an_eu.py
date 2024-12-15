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

#dataset
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
eu_medals = (
    medals
    .join(europe.rename({"Year": "eu_Year"}), on="Nation", how="left") 
    .filter(pl.col("Year") >= pl.col("eu_Year"))  
)

st.title("Analisi delle Medaglie Olimpiche in Unione Europea 🤝")


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


nations = eu_medals.select("Nation").unique().sort("Nation").to_series().to_list()

selected_nations = st.multiselect(
    "Seleziona uno o più stati",
    nations,
    max_selections = 4,
    default = ["Italy", "France", "Spain"]
)
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
                alt.Tooltip("Nation:N", title="Nazione"),
                alt.Tooltip("Type:N", title = "Tipo di medaglia"),
                alt.Tooltip("Count:Q", title = "Quantità")
            ]
        )
        .properties(title = "Confronto tra nazioni e tipologia di medaglie")
        .configure_title(anchor = "middle")
)

# Visualizzazione con Streamlit
st.altair_chart(chart, use_container_width=True)


chart = (
    alt.Chart(eu_medals)
    .mark_rect()
    .encode(
        alt.X("Year:O", title="Anno"),
        alt.Y("Nation:N", title="Nazione"),
        alt.Color("Total:Q", scale = alt.Scale(type = "log", scheme = "bluepurple"), title = "Totale medaglie"),
        tooltip=[
            alt.Tooltip("Nation:N", title="Nazione"),
            alt.Tooltip("Year:O", title="Anno"),
            alt.Tooltip("Total:Q", title="Totale medaglie")
        ]
    )
    .properties(title="Totale medaglie per anno e nazione")
    .configure_title(anchor = "middle")
)
st.altair_chart(chart, 
                use_container_width = True)

