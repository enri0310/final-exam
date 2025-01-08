import polars as pl
import utils_pl as utpl

def europe():
    path = "dataframes/europe.csv"
    data = utpl.load_csv(path)
    if data is not None:
        return data
    #provo a generazione dei dati
    try:
        data = get_eucountry()
        data.write_csv(path)
        print(f"Dati salvati in: {path}")
        return data
    except Exception as e:
        print(f"Errore durante la generazione o il salvataggio dei dati: {e}")
        return None
    
def get_eucountry():
    # URL della pagina Wikipedia
    url = "https://en.wikipedia.org/wiki/Member_state_of_the_European_Union"
    tables = utpl.download_table(url)

    if not tables:
        print(f"Nessuna tabella trovata in {url}")
        return None

    df = tables[1]

    #tidy dei dati
    df = df.with_columns(
        pl.col("Country").str.replace(r"\[.*?\]", "").alias("Nation"),
        pl.col("Accession").str.extract(r"(\d{4})", group_index=0).alias("year")
    )
    #creazione colonna year 
    df = df.with_columns(
        pl.when(pl.col("year").is_null()) 
        .then(1958)
        .otherwise(pl.col("year"))
        .alias("Year")
        .cast(pl.Int32)
    )

    return df.select(["Nation", "Year"])

def get_soviet():
    soviet = ["Soviet Union",
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
              "Tajikistan"
            ]
    return soviet

if __name__ == "__main__":
    df = europe()
    if df is not None:
        print(df)
