#!/usr/bin/env python3
import requests
import numpy as np
import pandas as pd
from pathlib import Path

csv_path = Path("csv")
out_path = Path("dataset.csv")

def download_all():
    # note: this step may overwrite some files in the csv directory
    week_number = 1
    while True:
        print("Download week", week_number, end="\r", flush=True)
        res = requests.get(f"https://www.stwno.de/infomax/daten-extern/csv/UNI-R/{week_number}.csv")
        if res.status_code != 200:
            break
        with open(csv_path/f"{week_number}.csv", "w") as f:
            f.write(res.content.decode("cp1252"))
        week_number += 1

def read_convert(csv_path):
    df = pd.read_csv(csv_path, delimiter=";")
    df.datum = df.datum.apply(lambda d: "-".join(d.split(".")[::-1])).astype("datetime64[ns]")
    df.stud = df.stud.str.replace(",", ".").astype(np.float)
    df.bed = df.bed.str.replace(",", ".").astype(np.float)
    df.gast = df.gast.str.replace(",", ".").astype(np.float)
    df = df.drop(columns=["preis"])
    return df

def merge(latest_date=None):
    frames = []
    for p in csv_path.iterdir():
        try:
            sub_df = read_convert(p)
            if latest_date is None or sub_df.datum.min() > latest_date:
                frames.append(sub_df)
        except pd.errors.EmptyDataError:
            print("Skip:", p, "is empty")
        except Exception as e:
            print("Skip: Unhandled error in", p)
            print(e)

    # also sort by name to get predictable results
    df = pd.concat(frames, ignore_index=True).sort_values(["datum", "name"])
    return df

def insert(csv_path):
    """Use this function to insert weeks that required a manual fix"""
    new_df = read_convert(csv_path)
    df = pd.read_csv(out_path)
    df.datum = df.datum.astype("datetime64[ns]")
    pd.concat([df, new_df], ignore_index=True).sort_values(["datum", "name"]).to_csv(out_path, index=False)

if __name__ == "__main__":
    csv_path.mkdir(exist_ok=True)
    download_all()
    # merge into existing data
    if out_path.exists():
        df = pd.read_csv(out_path)
        df.datum = df.datum.astype("datetime64[ns]")

        print("Merge")
        new_df = merge(df.datum.max())
        print("Concat")
        pd.concat([df, new_df], ignore_index=True).to_csv(out_path, index=False)
    else:
        merge().to_csv(out_path, index=False)
