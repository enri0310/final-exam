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

world = utl.get_geography()
chartwrl = (
    alt.Chart(world)
    .mark_geoshape()
    .encode(color = alt.value("lightgrey"))
    .properties(width = 600, height = 600)
)

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
chart = ((chartwrl + charteu )
         .properties(width = 600, height = 600)
         .project(
             type = "azimuthalEqualArea",
             scale = 800,
             center = (10, 48)
         )
)
#utl.open_map(chart, "eu_year")

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
chart = ((chartwrl + charteu )
         .properties(width = 600, height = 600)
         .project(
             type = "azimuthalEqualArea",
             scale = 800,
             center = (10, 48)
         )
)
utl.open_map(chart, "europe_medals")


