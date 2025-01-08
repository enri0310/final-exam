import polars as pl
import utils_pl as utpl
import polars as pl

def olympics():
    path = "dataframes/medals.csv"
    data = utpl.load_csv(path)
    if data is not None:
        return data
    #provo a generazione dei dati
    try:
        data = get_medals()
        data.write_csv(path)
        print(f"Dati salvati in: {path}")
        return data
    except Exception as e:
        print(f"Errore durante la generazione o il salvataggio dei dati: {e}")
        return None

def get_year(year):
    url = f"https://en.wikipedia.org/wiki/{year}_Summer_Olympics_medal_table"
    tables = utpl.download_table(url)

    if not tables:
        return None
    
    for df in tables:
        # verifico che il dataframe contenga le colonne desiderate
        if any("NOC" in col or "Nation" in col or 'Team' in col for col in df.columns) and any('Gold' in col for col in df.columns):           
            for col in df.columns:
                if 'NOC' in col or 'Team' in col:
                    df = df.rename({col: "Nation"})

            # tidy dei dati
            df = utpl.clean_column(df, "Nation")

            for column in ["Gold", "Silver", "Bronze", "Total"]:
                df = utpl.cast_column(df, column)
            
            # rimuovo riga dei totali e colonna del ranking
            df = df.filter(~pl.col("Nation").str.contains("Total|Sum"))
            df = df.drop("Rank")

            # aggiungo colonna dell'anno
            df = df.with_columns(pl.lit(year).alias("Year"))
            
            return df

    print(f"Nessun medagliere trovato per l'anno {year}")
    return None

def get_medals():
    years = list(range(1896, 2025, 4))
    all_data = []
    exclude_teams = [
        "Mixed team",
        "Independent Olympic Participants",
        "Refugee Olympic Team",
        "Individual Neutral Athletes",
        "Independent Olympic Athletes"
    ]

    renamed_teams = {
    "Australasia" : "Australia",
    "Bohemia" : "Czechoslovakia",
    "Formosa": "Chinese Taipei",
    "Russian Empire": "Russia",
    "ROC": "Russia",
    "British West Indies": "Jamaica",
    "United Team of Germany": "Germany",
    "Ceylon" : "Sri Lanka",
    "Macedonia": "North Macedonia",
    "FR Yugoslavia" : "Serbia and Montenegro",
    "Unified Team" : "Soviet Union"
    }

    for year in years:
        print(f"Scaricando i dati per {year}")
        data = get_year(year)
        
        if data is not None:
            all_data.append(data)
        else:
            print(f"Errore nel recupero dei dati per {year}")

    if not all_data:
        print("Nessun dato disponibile")
        return None
    
    data = utpl.concatenate_df(all_data)
    data = utpl.filter_teams(data, exclude_teams)
    return utpl.rename_nations(data, renamed_teams)

if __name__ == "__main__":
    olympics_data = olympics()
    if olympics_data is not None:
        print(olympics_data)
