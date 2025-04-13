from pybaseball import statcast, playerid_reverse_lookup
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import json
import os

def merge_ids_with_names(df, id_col, label):
    ids = df[id_col].dropna().unique().astype(int)
    lookup = playerid_reverse_lookup(ids, key_type="mlbam")
    lookup[f"{label}_name"] = (
        lookup["name_first"].str.title() + " " + lookup["name_last"].str.title()
    )
    return (
        pd.DataFrame({id_col: ids})
        .merge(lookup[["key_mlbam", f"{label}_name"]], left_on=id_col, right_on="key_mlbam", how="left")
        .rename(columns={"key_mlbam": "player_id"})[[f"{label}_name", id_col]]
        .dropna()
        .drop_duplicates()
        .rename(columns={id_col: "player_id", f"{label}_name": "name"})
        .to_dict("records")
    )

def update_cache():
    end = date.today()
    start = end + relativedelta(months=-1)
    print(f"[*] Fetching Statcast data from {start} to {end}")

    df = statcast(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
    os.makedirs("data", exist_ok=True)

    batters = merge_ids_with_names(df, "batter", "batter")
    pitchers = merge_ids_with_names(df, "pitcher", "pitcher")

    with open("data/batters.json", "w") as f:
        json.dump(batters, f)

    with open("data/pitchers.json", "w") as f:
        json.dump(pitchers, f)

    print(f"[✓] Saved {len(batters)} batters and {len(pitchers)} pitchers.")

if __name__ == "__main__":
    update_cache()
