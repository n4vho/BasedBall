from datetime import date, timedelta, datetime
from collections import defaultdict
import pandas as pd, time
import json, os
import pandas.errors as pderr
from pybaseball import statcast

TODAY = date.today()
ISO_TODAY = TODAY.isoformat()


START_OF_SEASON = f"{date.today().year}-03-01"  # crude but fine
YESTERDAY = (date.today() - timedelta(days=1)).isoformat()

def map_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["description"] = df["description"].astype(str).str.lower()
    # pitch-level buckets
    df["swinging_strike"] = df["description"].isin(["swinging_strike", "swinging_strike_blocked"]).astype(int)
    df["called_strike"]   = (df["description"] == "called_strike").astype(int)
    df["foul"]            = df["description"].isin(["foul", "foul_tip"]).astype(int)
    df["ball"]            = (df["description"] == "ball").astype(int)
    # contact types (count when present)
    df["ground_ball"]     = (df["bb_type"] == "ground_ball").astype(int)
    df["fly_ball"]        = (df["bb_type"] == "fly_ball").astype(int)
    df["line_drive"]      = (df["bb_type"] == "line_drive").astype(int)
    df["popup"]           = (df["bb_type"] == "popup").astype(int)
    return df

def compute_rates(df: pd.DataFrame):
    total = len(df)
    if total == 0:
        return {}
    cols = ["swinging_strike","called_strike","foul","ball","ground_ball","fly_ball","line_drive","popup"]
    return {k: round(float(df[k].sum())/total, 6) for k in cols}

def month_windows(start: date, end: date):
    cur = date(start.year, start.month, 1)
    while cur <= end:
        next_month = (cur.replace(day=28) + timedelta(days=4)).replace(day=1)
        win_start = max(start, cur)
        win_end   = min(end, next_month - timedelta(days=1))
        yield win_start.isoformat(), win_end.isoformat()
        cur = next_month

def safe_statcast_range(s, e, max_retries=3, sleep_sec=2):
    for attempt in range(1, max_retries+1):
        try:
            df = statcast(s, e, parallel=False)  # parallel off = fewer bad CSVs
            return df if df is not None else pd.DataFrame()
        except (pderr.ParserError, Exception) as err:
            if attempt == max_retries:
                print(f"[statcast] failed {s}->{e}: {err}")
                return pd.DataFrame()
            time.sleep(sleep_sec * attempt)

def fetch_league_df_szn(start_season:str) -> pd.DataFrame:
    start = datetime.fromisoformat(start_season).date()
    end   = date.today()
    frames = []
    for s, e in month_windows(start, end):
        df = safe_statcast_range(s, e)
        if not df.empty:
            frames.append(df)
        else:
            print(f"[statcast] empty window {s} to {e}, continuing…")
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def main():
    START_OF_SEASON = f"{date.today().year}-03-01"
    df = fetch_league_df_szn(START_OF_SEASON)  # <-- new chunked fetch

    # Fallback if nothing came back
    if df.empty:
        y = (date.today() - timedelta(days=1)).isoformat()
        df = statcast(y, y, parallel=False)

    df = map_outcomes(df)

    overall = compute_rates(df)

    by_pitch = {}
    if "pitch_name" in df.columns:
        sub = df[df["pitch_name"].notna()]
        for pitch, g in sub.groupby("pitch_name"):
            by_pitch[pitch] = compute_rates(g)

    out = {
        "computed_on": ISO_TODAY,
        "overall": overall,
        "by_pitch": by_pitch
    }

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    with open(os.path.join(data_dir, "league_avg.json"), "w") as f:

        json.dump(out, f, indent=2)

if __name__ == "__main__":
    main()
