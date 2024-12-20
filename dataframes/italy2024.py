import utils_pl as utpl
import re
import polars as pl

def italy():
    path = "dataframes/italy2024.csv"
    data = utpl.load_csv(path)
    if data is not None:
        return data
    #provo a generazione dei dati
    try:
        data = get_italy()
        data.write_csv(path)
        print(f"Dati salvati in: {path}")
        return data
    except Exception as e:
        print(f"Errore durante la generazione o il salvataggio dei dati: {e}")
        return None

def get_italy():
    path = "dataframes/italy2024.txt"
    lines = utpl.read_tlines(path)
    if not lines:
        print(f"Nessuna tabella trovata in {path}")
        return None
    region_pattern = re.compile(r"^(.*?)(\(\d+\))$")
    athlete_pattern = re.compile(r"^(.*?)(\(.+\))$") 
    medals_data = []
    region = None

    for line in lines:
        is_region = region_pattern.match(line)
        if is_region:
            region = is_region.group(1)
        elif region and "(" in line:
            is_athlete = athlete_pattern.match(line)
            if is_athlete:
                athlete = is_athlete.group(1)
                details = is_athlete.group(2).strip("()")
                d_parts = details.split(" e ")
                for part in d_parts:
                    if "," in part:
                        description, city = part.rsplit(",", 1)
                        gold = "oro" in description.lower()
                        silver = "argento" in description.lower()
                        bronze = "bronzo" in description.lower()
                        medals_data.append({
                            "Athlete": athlete,
                            "City": city,
                            "Region": region,
                            "Gold": 1 if gold else 0,
                            "Silver": 1 if silver else 0,
                            "Bronze": 1 if bronze else 0,
                            "Total": 1
                        })
                    else:
                        description = part.strip()
                        gold = "oro" in description.lower()
                        silver = "argento" in description.lower()
                        bronze = "bronzo" in description.lower()
                        medals_data.append({
                            "Athlete": athlete,
                            "City": "",
                            "Region": region,
                            "Gold": 1 if gold else 0,
                            "Silver": 1 if silver else 0,
                            "Bronze": 1 if bronze else 0,
                            "Total": 1
                        })
            else:
                print(f"Riga non valida o senza regione associata: {line}")

    df = pl.DataFrame(medals_data)
    athlete = (df
               .group_by("Athlete")
               .agg([
                   pl.sum("Gold"),
                   pl.sum("Silver"),
                   pl.sum("Bronze"),
                   pl.sum("Total")
               ])
               .sort("Total", descending = True)
    )
    df = df.filter(pl.col("City").is_not_null() & (pl.col("City") != ""))

    df = athlete.join(
        df.select(pl.col("City"), pl.col("Region"), pl.col("Athlete")), 
        on = "Athlete",
        how = "left"
    )
    print(df.columns)
    df = df.with_columns([pl.col(column).str.strip_chars(" ") for column in df.columns if df.schema[column] == pl.Utf8])
    return df 


if __name__ == "__main__":
    df = italy()
    if df is not None:
        print(df)
