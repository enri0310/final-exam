import polars as pl
import pandas as pd
import requests
import os

def load_csv(file_path):
    if os.path.exists(file_path):
        #print(f"Caricando il file esistente: {file_path}")
        # Legge il CSV e restituisce i dati
        return pl.read_csv(file_path, null_values=["NA", ""])
    return None

# Ottiene tabelle HTML e le converte in Polars
def download_table(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Errore nell'accesso a {url}")
        return None

    tables = pd.read_html(url)
    if not tables:
        print(f"Nessuna tabella trovata in {url}")
        return None

    return [pl.from_pandas(table) for table in tables]

# Rinomina nazioni
def rename_nations(df, renamed_dict):
    if "Nation" in df.columns:  # Verifica che la colonna esista
        return df.with_columns(
            pl.col("Nation")
            .map_elements(lambda x: renamed_dict.get(x, x), return_dtype=pl.Utf8)  # Specifica il tipo di ritorno
            .alias("Nation")
        )
    else:
        raise ValueError("La colonna 'Nation' non è presente nel DataFrame.")

# Filtra nazioni
def filter_teams(df, exclude_teams):
    return df.filter(~pl.col("Nation").is_in(exclude_teams))

# Pulisce la colonna 
def clean_column(df, column_name):
    df = df.with_columns(pl.col(column_name)
        .str.replace(r"\s*\(.*\)", "", literal=False)  # Rimuove testo tra parentesi tonde
        .str.replace(r"\s*\[.*\]", "", literal=False)  # Rimuove testo tra parentesi quadre
        .str.replace(r"\*", "", literal=False)         # Rimuove asterischi
        .str.replace(r"\*|\.mw-parser-output.*", "", literal=False)  # Rimuove specifico pattern
        .str.strip_chars_end("‡*")                    # Rimuove caratteri ‡ e * dalla fine
        .str.strip_chars(" ")                         # Rimuove spazi in eccesso
    )
    return df

# Cast della colonna
def cast_column(df, column, dtype=pl.Int64, fill_value=0):
     df = df.with_columns(
                    pl.col(column).cast(dtype).fill_null(fill_value)
                )
     return df

# Crea unico dataframe
def concatenate_df(dfs):
    if not dfs:
        return None
    return pl.concat(dfs)