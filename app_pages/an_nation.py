import streamlit as st
import polars as pl
import altair as alt
import utils as utl
import pandas as pd
import polars.selectors as cs
from great_tables import loc, style, GT, md
import utils

utl.setup_page(
    title = "Nazioni",
    icon = "🏅",
    layout = "centered",
    css_file = "styles.css"
)

st.title("Analisi delle Medaglie Olimpiche per Nazione")

#dataset
medals = st.session_state.medal

# ordino in base alla modalità scelta
option = st.selectbox("Seleziona un criterio per ordinare:", ["Total", "Gold", "Silver", "Bronze"])
top_nations = (medals
              .group_by("Nation")
              .agg([pl.col("Gold").sum().alias("Gold"),
                    pl.col("Silver").sum().alias("Silver"),
                    pl.col("Bronze").sum().alias("Bronze"),
                    pl.col("Total").sum().alias("Total")]
              )
)

sub_title = ""
if option == "Total":
    criteria = ["Total", "Gold", "Silver", "Bronze"]
    sub_title = "Top **10** nazioni ordinate per n° Totale di medaglie vinte"
elif option == "Gold":
    criteria = ["Gold", "Total", "Silver", "Bronze"]
    sub_title = "Top **10** nazioni ordinate per n° di Ori vinti"
elif option == "Silver":
    criteria = ["Silver", "Gold", "Total", "Bronze"]
    sub_title = "Top **10** nazioni ordinate per n° di Argenti vinti"
elif option == "Bronze":
    criteria = ["Bronze", "Gold", "Silver", "Total"]
    sub_title = "Top **10** nazioni ordinate per n° di Bronzi vinti"
top_nations = top_nations.sort(by = criteria, descending = [True] * 4)

# metto colonna rank all'inizio del df
col_rank = pl.Series("Rank", list(range(1, len(top_nations) + 1)))
top_nations = top_nations.insert_column(0, col_rank)
top_table = (
    GT(data = top_nations.head(10))
    .tab_header(
        title= md("Medagliere olimpico *Mondiale* &#x1F310;"),
        subtitle=md("")
    )
    .tab_spanner(label="Nazione", columns=["Rank","Nation"])
    .tab_spanner(label="Medaglie", columns=["Gold", "Silver", "Bronze", "Total"])
    .tab_style(
        style.fill("yellow"),
    loc.body(
        columns=cs.all(),
        rows=pl.col("Nation") == "Italy"
    )
).tab_style(
    style.text(align = "center"),
    loc.spanner_labels(["Medaglie"])
).tab_style(
    style.text(weight="bold"),
    loc.column_labels(option)
).tab_style(
    style.text(align = "center"),
    loc.source_notes()
)
    .tab_source_note(
        source_note=md("Source: **Wikipedia** - Olympic Medal Counts by Country.")
    )
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
                 alt.Color("Type")
             )
             .properties(width = 180, height = 220)
)
text_chart = (base_pie
              .mark_text(radius = 80)
              .encode(
                  alt.Theta("Frac", stack=True),
                  alt.Text("Count"),
                  alt.Order("Type")
              )
)
big_text_chart = (alt.Chart(pie_data)
                  .mark_text(size = 20, radius = 0)
                  .encode(alt.Text("Total"))
)

st.altair_chart((pie_chart + text_chart + big_text_chart)
                .facet(
                    alt.Row("Nation", title = None), 
                    columns = 5, 
                    spacing = 10, 
                    bounds = "flush")
                .properties(title = "Distribuzione delle Medaglie per Tipo di Nazione")
)

#edizioni olimpiche
nation_editions = (medals
                   .group_by("Nation")
                   .agg([pl.col("Year").n_unique().alias("Ol_ed")])
)
top_nations = top_nations.join(nation_editions, on = "Nation")

# creazione di un df per tutti gli anni in cui si sono svolte le olimpiadi e lista di tutte le nazioni
years = medals.select("Year").unique().sort("Year").to_series().to_list()
df_years = pl.DataFrame({"Year": years})
df_noyears = pl.DataFrame({"Year": [1916, 1940, 1944]})
df_allyears = pl.concat([df_years, df_noyears]).sort("Year")
nations = medals.select("Nation").unique().sort("Nation").to_series().to_list()


st.markdown("""<h3> 📈 Serie Temporale delle Medaglie per Nazione </h3>""",
            unsafe_allow_html = True)

# selectbox
selected_nation = st.selectbox(
    "Seleziona una nazione:",
    nations,
    index = nations.index("Italy")
)
# selezione nazione e aggregazione per anno 
ts_data = (medals
           .filter(pl.col("Nation") == selected_nation)
           .group_by("Year")
           .agg([
               pl.col("Gold").sum().alias("Gold"),
               pl.col("Silver").sum().alias("Silver"),
               pl.col("Bronze").sum().alias("Bronze"),
               pl.col("Total").sum().alias("Total")
           ])       
)
ts_data = (
    df_years
    .join(ts_data, on = "Year", how = "left")
    .fill_null(0)
)
# creo serie temporale
data_chart = (
    alt.Chart(ts_data)
    .mark_line()
    .transform_filter("datum.Total > 0")
    .encode(
        alt.X("Year:O", title = "Anno", axis = alt.Axis(values = years)),
        alt.Y("Total:Q", title = "Totale Medaglie"),
        alt.Color(value = "#1f77b4"),
        alt.Tooltip(["Year", "Gold", "Silver", "Bronze", "Total"])
    )
)
point_chart = (
    alt.Chart(ts_data)
    .mark_point(size = 50)
    .encode(
        alt.X("Year:O", title = "Anno"),
        alt.Y("Total:Q"),
        alt.Tooltip(["Year", "Gold", "Silver", "Bronze", "Total"]),
        color = alt.condition("datum.Total > 0", alt.value("#1f77b4"), alt.value("#d62728"))
    )
)
# aggiungo anni in cui non sono avvenute le olimpiadi
year_chart = (
    alt.Chart(df_noyears)
    .mark_rect(opacity = 0.4, color = "red") 
    .encode(alt.X("Year:O"))
)
st.altair_chart(
    (year_chart + data_chart + point_chart).properties(title = f"Serie Temporale delle Medaglie - {selected_nation}"),
    use_container_width = True
)


st.markdown("""<h3> 📈 Paragone delle Medaglie tra le Nazioni </h3>""",
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
    alt.Chart(df_years)
    .mark_point(opacity = 0) 
    .encode(alt.X("Year:O", title = "Anno"))
)
data_chart = (
    alt.Chart(ts_data)
    .mark_line()
    .encode(
        alt.X("Year:O", title = "Anno", axis = alt.Axis(values = years)),
        alt.Y("Total:Q", title = "Totale Medaglie"),
        alt.Color("Nation:N", scale = alt.Scale(scheme = "viridis"), title = "Nazione"),
        alt.Tooltip(["Nation", "Year", "Gold", "Silver", "Bronze", "Total"])
    )
)
point_chart = (
    alt.Chart(ts_data)
    .mark_point(size = 50)
    .encode(
        alt.X("Year:O", title = "Anno", axis = alt.Axis(values = years)),
        alt.Y("Total:Q"),
        alt.Color("Nation:N", title = "Nazione"),  # Distinzione per nazione
        alt.Tooltip(["Nation", "Year", "Gold", "Silver", "Bronze", "Total"])
    )
)
st.altair_chart(
    (empty_chart + data_chart + point_chart + year_chart).properties(title = f"Serie Temporale delle Medaglie - {', '.join(selected_nations)}"),
    use_container_width = True
)



# Numero di edizioni per cui ogni nazione ha vinto medaglie
scatter_chart = (alt.Chart(top_nations)
                 .mark_circle(size = 100, opacity = 0.8, stroke = 'black', strokeWidth = 1)
                 .encode(
                     alt.X('Ol_ed:Q', title='Numero di Edizioni Olimpiche'),
                     alt.Y('Total:Q', title='Totale Medaglie'),
                     alt.Color('Total:Q', scale=alt.Scale(scheme='greens'), title='Totale Medaglie'),
                     tooltip = [
                         alt.Tooltip('Nation:N', title='Nazione'),
                         alt.Tooltip('Total:Q', title='Totale Medaglie'),
                         alt.Tooltip('Ol_ed:Q', title='Numero di Edizioni Olimpiche')
                     ]
                 )
                 .properties(
                     title = 'Relazione tra Numero di Medaglie e Numero di Edizioni Olimpiche per Nazione',
                     width = 600,
                     height = 400
                 )
)
st.altair_chart(scatter_chart, use_container_width=True)



# Grafico di dispersione con un modello lineare
scatter_chart_with_regression = (alt.Chart(top_nations)
    .mark_circle(size=100, opacity=0.8, stroke='black', strokeWidth=1)
    .encode(
        alt.X('Ol_ed:Q', title='Numero di Edizioni Olimpiche'),
        alt.Y('Total:Q', title='Totale Medaglie'),
        alt.Color('Total:Q', title='Totale Medaglie'),
        tooltip=[
            alt.Tooltip('Nation:N', title='Nazione'),
            alt.Tooltip('Total:Q', title='Totale Medaglie'),
            alt.Tooltip('Ol_ed:Q', title='Numero di Edizioni Olimpiche')
        ]
    )
    .properties(
        title='Relazione tra Numero di Medaglie e Numero di Edizioni Olimpiche per Nazione',
        width=600,
        height=400
    )
)
top_nations
# Aggiunta del modello lineare (regressione)
points = alt.Chart(top_nations).mark_point().encode(
    x=alt.X('Ol_ed:Q', title='Edizioni Partecipate'),
    y=alt.Y('Total:Q', title='Medaglie Totali'),
    tooltip=['Nation', 'Ol_ed', 'Total']
).properties(
    title='Relazione tra edizioni olimpiche partecipate e medaglie totali',
    width=800,
    height=400
)

# Aggiunta della linea di regressione
regression_line = points.transform_regression('Ol_ed', 'Total').mark_line(color='red', size=2)

# Combinazione del grafico
final_chart = points + regression_line

# Mostra il grafico

# Visualizzare il grafico
st.altair_chart(final_chart, use_container_width=True)
