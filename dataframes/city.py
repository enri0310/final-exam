import utils_pl as utpl

def cities():
    path = "dataframes/cities.csv"
    data = utpl.load_csv(path)
    if data is not None:
        return data
    #provo a generazione dei dati
    try:
        data = get_cities()
        data.write_csv(path)
        print(f"Dati salvati in: {path}")
        return data
    except Exception as e:
        print(f"Errore durante la generazione o il salvataggio dei dati: {e}")
        return None

def get_cities():
    url = "https://en.wikipedia.org/wiki/List_of_Olympic_Games_host_cities"
    tables = utpl.download_table(url)

    if not tables:
        print(f"Nessuna tabella trovata in {url}")
        return None

    #cerca la tabella con città ospitanti
    for df in tables:
        if any("City" in col for col in df.columns) and any("Country" in col for col in df.columns) \
            and any("Year" in col for col in df.columns) and any("Region" in col for col in df.columns) \
            and any("Opening ceremony" in col for col in df.columns) and any("Closing ceremony" in col for col in df.columns) :           
            
            df = df.select(["City.1", "Country", "Year", "Region", "Opening ceremony", "Closing ceremony"])
            df = df.rename({"City.1" : "City"})
            
            # tidy dei dati
            for column in ["City", "Country", "Opening ceremony", "Closing ceremony"]:
                df = utpl.clean_column(df, column)

            return df
        
    return None


if __name__ == "__main__":
    df = cities()
    if df is not None:
        print(df)
