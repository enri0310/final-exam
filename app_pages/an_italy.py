import streamlit as st
import polars as pl
import altair as alt
import utils as utl

utl.setup_page(
    title="Italia",
    icon="🇮🇹",
    layout="centered"
)

#dataset
medals = st.session_state.medal
medals = medals.filter(pl.col("Nation") == "Italy")
italy2024 = st.session_state.italy2024
df_allyears = pl.DataFrame({"Year": list(range(1896, 2025, 4))})

st.title("Analisi delle Medaglie Olimpiche in Italia 🍕")

st.metric(
    label="Nazioni Partecipanti",
    value=None
)
st.metric(
    label="Nazioni Vincitrici",
    value=None
)


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
                     "Type", 
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



sort_chart = (
    italy2024
    .group_by("Region")
    .agg([
        pl.col("Gold").sum(),
        pl.col("Silver").sum(),
        pl.col("Bronze").sum(),
        pl.col("Total").sum()
    ])
    .with_columns( 
        (pl.col("Total") * 100000 +
         pl.col("Gold") * 1000 + 
         pl.col("Silver") * 10 + 
         pl.col("Bronze")).alias("Weight") 
    )
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
bar_chart = (alt.Chart(data_chart)
             .mark_bar()
             .encode(
                 alt.X("Count:Q", title="Numero di medaglie"),
                 alt.Y("Region:N", sort = alt.SortField(field = "Weight", order = "descending"), title = None),
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
                  alt.Y("Region:N", sort = alt.SortField(field = "Weight", order = "descending")),
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
