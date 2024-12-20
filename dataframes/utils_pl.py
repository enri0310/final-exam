import polars as pl
import pandas as pd
import requests
import os

def load_csv(file_path):
    if os.path.exists(file_path):
        #print(f"Caricando il file esistente: {file_path}")
        return pl.read_csv(file_path, null_values = ["NA", ""])
    return None

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

def read_tlines(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return lines
    except Exception as e:
        print(f"Errore nella lettura del file {file_path}: {e}")
        return None

def rename_nations(df, renamed_dict):
    if "Nation" in df.columns:  
        return df.with_columns(
            pl.col("Nation")
            .map_elements(lambda x: renamed_dict.get(x, x), return_dtype = pl.Utf8) 
            .alias("Nation")
        )
    else:
        raise ValueError("La colonna 'Nation' non è presente nel DataFrame.")

def filter_teams(df, exclude_teams):
    return df.filter(~pl.col("Nation").is_in(exclude_teams))

def clean_column(df, column_name):
    df = df.with_columns(pl.col(column_name)
        .str.replace(r"\s*\(.*\)", "", literal = False)  
        .str.replace(r"\s*\[.*\]", "", literal = False)  
        .str.replace(r"\*", "", literal = False)         
        .str.replace(r"\*|\.mw-parser-output.*", "", literal = False)
        .str.strip_chars_end("‡*")                   
        .str.strip_chars(" ")                         
    )
    return df

def cast_column(df, column, dtype = pl.Int64, fill_value = 0):
     df = df.with_columns(pl.col(column).cast(dtype).fill_null(fill_value))
     return df

def concatenate_df(dfs):
    if not dfs:
        return None
    return pl.concat(dfs)