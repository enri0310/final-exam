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
    layout = "centered",
    css_file = "styles.css"
)

#dataset
medals = st.session_state.medal
medals = medals.with_columns(
    pl.col("Nation").alias("old_nation")
)
cities = st.session_state.city
cities = cities.with_columns(
    pl.col("Nation").alias("old_nation")
)
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
        medals = medals.with_columns(
            pl.col("old_nation").alias("Nation")
        )
        cities = cities.with_columns(
            pl.col("old_nation").alias("Nation")
        )
medals = (medals
              .group_by(["Nation", "Year"])
              .agg([pl.col("Gold").sum().alias("Gold"),
                    pl.col("Silver").sum().alias("Silver"),
                    pl.col("Bronze").sum().alias("Bronze"),
                    pl.col("Total").sum().alias("Total")]
              )
)
st.title("Analisi delle medaglie olimpiche nel Mondo 🌍")

years = medals.select("Year").unique().sort("Year").to_series().to_list()
df_years = pl.DataFrame({"Year": years})
noyears = [year for year in list(range(1896, 2025, 4))  if year not in years]
df_noyears = pl.DataFrame({"Year": noyears})
df_allyears = pl.concat([df_years, df_noyears]).sort("Year")

nations = medals.select("Nation").unique().sort("Nation").to_series().to_list()

medals = medals.with_columns((pl.col("Gold") / pl.col("Total") * 100).alias("Gold%"))
top_nations = (medals
              .group_by("Nation")
              .agg([pl.col("Gold").sum().alias("Gold"),
                    pl.col("Silver").sum().alias("Silver"),
                    pl.col("Bronze").sum().alias("Bronze"),
                    pl.col("Total").sum().alias("Total")]
              )
)

cities = cities.filter(~pl.col("Summer").is_null())
cities = cities.filter(~pl.col("Year").is_in(noyears))
cities = cities.filter(pl.col("Year").is_in(years))
cities = cities.select(pl.col("City"), 
                       pl.col("Nation"), 
                       pl.col("Year"), 
                       pl.col("Region"), 
                       pl.col("Opening ceremony"), 
                       pl.col("Closing ceremony"))
cities = cities.with_columns(
    pl.col("Opening ceremony")
    .str.strptime(pl.Date, "%d %B %Y", strict = False)
    .alias("Opening date"),
    
    pl.col("Closing ceremony")
    .str.strptime(pl.Date, "%d %B %Y", strict = False)
    .alias("Closing date")   
)
cities = cities.with_columns(
    ((pl.col("Closing date") - pl.col("Opening date"))
     .cast(pl.Int64)/ (1000 * 60 * 60 * 24) + 1)
     .cast(pl.Int64)
     .alias("Days")
)


#SEZIONE PER NAZIONE
st.markdown("""<h2>• Analisi per Nazione </h2>""",
            unsafe_allow_html = True)

st.markdown("""<h3> 📊 Top 10 Nazioni per totale di medaglie </h3>""",
            unsafe_allow_html = True)
# ordino in base alla modalità scelta
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

# metto colonna rank all'inizio del df
col_rank = pl.Series("Rank", list(range(1, len(top_nations) + 1)))
top_nations = top_nations.insert_column(0, col_rank)
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

#creo grafici a torta delle top 10 nazioni
pie_data = (top_nations
            .head(10)
            .with_columns(
                (pl.col("Gold") / pl.col("Total") * 100).round(decimals=2).cast(pl.Float64).alias("Gold_f"),
                (pl.col("Silver") / pl.col("Total") * 100).round(decimals=2).cast(pl.Float64).alias("Silver_f"),
                (pl.col("Bronze") / pl.col("Total") * 100).round(decimals=2).cast(pl.Float64).alias("Bronze_f")
            )
            .unpivot(
                index = "Nation",
                on = ["Gold_f", "Silver_f", "Bronze_f"],
                value_name = "Frac",
                variable_name = "Type"
            )
            .with_columns(
                pl.col("Type").str.replace("_f", "", literal=False),
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
             .mark_arc(radius = 50, radius2 = 70, cornerRadius = 10)
             .encode(
                 alt.Theta("Frac"),
                 alt.Color(
                     "Type", 
                     scale = alt.Scale(domain = ["Gold", "Silver", "Bronze"],range = ["gold", "silver", "brown"]),
                     legend = None
                 ),
                 alt.Order("Order", sort = "ascending"),
                 tooltip = [                   
                     alt.Tooltip("Type", title = "Tipologia"),
                     alt.Tooltip("Frac", title = "%"),
                 ]
             )
             .properties(width = 180, height = 220)
)
text_chart = (base_pie
              .mark_text(radius = 85)
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



st.markdown("""<h3> 📈 Serie temporale delle medaglie </h3>""",
            unsafe_allow_html = True)
selected_nations = st.multiselect(
    "Seleziona uno o più stati",
    nations,
    max_selections = 4,
    default = "Italy"
)
# selezione delle nazioni e aggregazione per anno
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
# creo serie temporale
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
# aggiungo anni in cui non sono avvenute le olimpiadi
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
# aggiungo il numero di edizioni olimpiche partecipate al df
nation_editions = (medals
                   .group_by("Nation")
                   .agg([pl.col("Year").n_unique().alias("Ol_ed")])
)
top_nations = top_nations.join(nation_editions, on = "Nation")
# trasformo in logartimo
top_nations = top_nations.with_columns(
    (pl.col("Total").log()).alias("Log_Total")
)
# creo modello lineare
x = top_nations["Ol_ed"].to_numpy()
y = top_nations["Log_Total"].to_numpy()
x = sm.add_constant(x)
model = sm.OLS(y, x).fit()
beta_0 = np.exp(model.params[0])
beta_1 = model.params[1]
# aggiungo valori predetti al df
top_nations = top_nations.with_columns(
    (beta_0 * np.exp(beta_1 * pl.col("Ol_ed"))).alias("Predicted")
)

# creo grafico
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


#SEZIONE PER EDIZIONE
st.markdown("""<h2>• Analisi per Edizione </h2>""",
            unsafe_allow_html = True)

st.markdown("""<h3> 📊 Top 10 Nazioni per totale di medaglie per edizione </h3>""",
            unsafe_allow_html = True)
year = st.selectbox("Seleziona l'anno:", years)
top_10year = (medals
        .filter(pl.col("Year") == year)
        .sort("Total", descending = True).head(10)
        )
chart = (
    alt.Chart(top_10year)
    .mark_bar()
    .encode(
        alt.X("Nation", sort="-y", title="Nazione"),
        alt.Y("Total", title="Totale medaglie"),
        alt.Color("Gold%", title="% Medaglie d'Oro", scale=alt.Scale(scheme="goldorange", domain=[0, 100])),
        tooltip=[
            alt.Tooltip("Nation:N", title = "Nazione"),
            alt.Tooltip("Gold:Q", title = "Ori"),
            alt.Tooltip("Silver:Q", title = "Argenti"),
            alt.Tooltip("Bronze:Q", title = "Bronzi"),
            alt.Tooltip("Total:Q", title = "Totale")
        ])
    )
st.altair_chart(chart, 
                use_container_width = True)



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



region_data = (
    cities
    .group_by("Region")
    .agg(pl.col("Year").count().alias("Count"))
    .sort("Count", descending=True)
)
pie_chart = (
    alt.Chart(region_data)
    .mark_arc(radius = 70, radius2 = 100, cornerRadius = 10)
    .encode(
        alt.Theta("Count:Q", title = "Numero di edizioni"),
        alt.Color("Region:N", title = "Contiente"),
        alt.Order("Count:Q", sort = "descending"),
        tooltip=[
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


host_nations = cities.select("Nation").unique().sort("Nation").to_series().to_list()
all_continents = cities.select("Region").unique().to_series().to_list()
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
host_perf = (
    medals
    .join(cities,
        on = ["Year", "Nation"],
        how = "left")
    .filter(~pl.col("City").is_null())
)
host_perf1 = host_perf.filter(pl.col("Nation").is_in(g1))
host_perf2 = host_perf.filter(pl.col("Nation").is_in(g2))
boxplot1 = (
    alt.Chart(g1_medals)
    .mark_boxplot(size = 45)
    .encode(
        alt.X("Nation:N"),  
        alt.Y("Total:Q", title = "Totale medaglie", scale = alt.Scale(domain = [0, 240])),
        alt.Color(
            "Region:N",
            title="Continente",
            scale=alt.Scale(domain = all_continents), 
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
    .mark_point(shape = "circle", size = 100, filled = True)
    .encode(
        alt.X("Nation:N"),
        alt.Y("Total:Q"),
        color = alt.value("purple"),
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
    .mark_point(shape = "circle", size = 100, filled = True)
    .encode(
        alt.X("Nation:N"),
        alt.Y("Total:Q"),
        color = alt.value("purple"),
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
