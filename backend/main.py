from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json, os, time
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from pybaseball import statcast, statcast_batter, statcast_pitcher, playerid_reverse_lookup, playerid_reverse_lookup
from collections import defaultdict
from routes import batter_profile, pitcher_profile
import numpy as np
import pandas as pd, time
import pandas.errors as pderr

app = FastAPI()

app.include_router(batter_profile.router)
app.include_router(pitcher_profile.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://based-ball.vercel.app",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic model BEFORE using it
class MatchupRequest(BaseModel):
    batter: str
    pitcher: str
    pitch_type: str = ""

@app.get("/api/players/batters")
def get_batters():
    with open("data/batters.json", "r") as f:
        return json.load(f)

@app.get("/api/players/pitchers")
def get_pitchers():
    with open("data/pitchers.json", "r") as f:
        return json.load(f)

def calculate_outcomes(df):
    """
    Per-pitch outcome space (NO 'strikeout' here):
      swinging_strike, called_strike, foul, ball,
      ground_ball, fly_ball, line_drive, popup
    Returns per-pitch rates over ALL pitches in the df.
    """
    outcome_counts = defaultdict(int)
    total = 0

    for _, row in df.iterrows():
        des = str(row.get("description", "")).lower()
        bb = row.get("bb_type")

        # pitch-level results
        if des in ("swinging_strike", "swinging_strike_blocked"):
            outcome_counts["swinging_strike"] += 1
        elif des == "called_strike":
            outcome_counts["called_strike"] += 1
        elif des in ("foul", "foul_tip"):
            outcome_counts["foul"] += 1
        elif des == "ball":
            outcome_counts["ball"] += 1

        # contact types (count when present)
        if bb == "ground_ball":
            outcome_counts["ground_ball"] += 1
        elif bb == "fly_ball":
            outcome_counts["fly_ball"] += 1
        elif bb == "line_drive":
            outcome_counts["line_drive"] += 1
        elif bb == "popup":
            outcome_counts["popup"] += 1

        total += 1

    return {k: (v / total) for k, v in outcome_counts.items()} if total > 0 else {}

# Helper to group by pitch type
def group_by_pitch(df):
    grouped = {}
    for pitch_type, group in df.groupby("pitch_name"):
        outcomes = calculate_outcomes(group)
        grouped[pitch_type] = {
            "usage": len(group),
            "outcomes": outcomes
        }
    return grouped


# league_avg = {
#   "strikeout": 0.22,
#   "ground_ball": 0.28,
#   "fly_ball": 0.25,
#   "line_drive": 0.18,
#   "popup": 0.05
# }

def load_league_avg():
    try:
        with open("data/league_avg.json") as f:
            return json.load(f)
    except:
        # safe defaults if file missing
        return {"overall":{
            "swinging_strike":0.115,"called_strike":0.175,"foul":0.150,"ball":0.340,
            "ground_ball":0.090,"fly_ball":0.045,"line_drive":0.030,"popup":0.010
        }, "by_pitch":{}}



def log5(batter_rate, pitcher_rate, league_rate):
    num = batter_rate * pitcher_rate
    denom = num + (1 - batter_rate) * (1 - pitcher_rate) / league_rate
    return num / denom if denom else 0.0


@app.post("/api/matchup")
def evaluate_matchup(req: MatchupRequest):
    print("REQ:", req.batter, req.pitcher, req.pitch_type)
    print(f"[*] Simulating: {req.batter} vs {req.pitcher}")
    start = "2023-01-01"
    end = str(date.today())

    # ID lookup
    with open("data/batters.json") as f:
        batters = json.load(f)
    with open("data/pitchers.json") as f:
        pitchers = json.load(f)

    batter_id = next((p["player_id"] for p in batters if p["name"] == req.batter), None)
    pitcher_id = next((p["player_id"] for p in pitchers if p["name"] == req.pitcher), None)
    if not batter_id or not pitcher_id:
        return {"error": "Player ID not found"}

    # Pull Statcast
    batter_df = statcast_batter(start, end, batter_id)
    pitcher_df = statcast_pitcher(start, end, pitcher_id)

    batter_by_pitch = group_by_pitch(batter_df)
    pitcher_by_pitch = group_by_pitch(pitcher_df)

    # League averages (overall + by pitch)
    league = load_league_avg()

    total_pitch_usage = sum(v["usage"] for v in pitcher_by_pitch.values())
    if total_pitch_usage == 0:
        return {"error": "Pitcher has no pitch data"}

    combined = defaultdict(float)  # numeric outcomes only here

    # ---- pitch selected: blend only that pitch ----
    if req.pitch_type:
        pitch = req.pitch_type
        if pitch not in batter_by_pitch or pitch not in pitcher_by_pitch:
            return {"error": f"No shared data for pitch type: {pitch}"}

        b_outcomes = batter_by_pitch[pitch]["outcomes"]
        p_outcomes = pitcher_by_pitch[pitch]["outcomes"]

        keys = set(b_outcomes.keys()).union(p_outcomes.keys())

        for outcome in keys:
            b_val = b_outcomes.get(outcome, 0.0)
            p_val = p_outcomes.get(outcome, 0.0)
            # pitch-aware league baseline → fallback to overall
            L = league["by_pitch"].get(pitch, {}).get(outcome, league["overall"].get(outcome, 0.001))
            blended = log5(b_val, p_val, L)
            combined[outcome] = blended  # don't round yet

        # attach a sample-size note (added AFTER normalization below)
        note_b = batter_by_pitch[pitch]["usage"]
        note_p = pitcher_by_pitch[pitch]["usage"]
        sample_note = f"* Based on {note_b} batter pitches and {note_p} pitcher pitches for {pitch}."

    # ---- no pitch selected: usage-weighted blend over all shared pitches ----
    else:
        for pitch, pdata in pitcher_by_pitch.items():
            if pitch not in batter_by_pitch:
                continue

            b_outcomes = batter_by_pitch[pitch]["outcomes"]
            p_outcomes = pdata["outcomes"]
            usage_weight = pdata["usage"] / total_pitch_usage

            keys = set(b_outcomes.keys()).union(p_outcomes.keys())

            for outcome in keys:
                b_val = b_outcomes.get(outcome, 0.0)
                p_val = p_outcomes.get(outcome, 0.0)
                L = league["by_pitch"].get(pitch, {}).get(outcome, league["overall"].get(outcome, 0.001))
                blended = log5(b_val, p_val, L)
                combined[outcome] += blended * usage_weight  # accumulate weighted

        sample_note = None  # not a single pitch

    # ---- normalize numeric outcomes ONLY ----
    numeric_keys = [k for k, v in combined.items() if isinstance(v, (int, float))]
    if not numeric_keys:
        return {"error": "No overlapping pitch data"}

    total = sum(combined[k] for k in numeric_keys)
    if total == 0:
        return {"error": "No overlapping pitch data"}

    for k in numeric_keys:
        combined[k] = round(combined[k] / total, 4)

    # in_play = sum of contact buckets (pitch-level view)
    combined["in_play"] = round(
        combined.get("ground_ball", 0.0)
      + combined.get("fly_ball", 0.0)
      + combined.get("line_drive", 0.0)
      + combined.get("popup", 0.0), 4
    )

    # add meta AFTER normalization so they don't pollute totals
    if sample_note:
        combined["note"] = sample_note

    combined["league_updated"] = league.get("computed_on")

    return combined

@app.get("/api/pitch-types/{pitcher_name}")
def get_pitch_types(pitcher_name: str):
    # find pitcher id
    with open("data/pitchers.json") as f:
        pitchers = json.load(f)
    pitcher_id = next((p["player_id"] for p in pitchers if p["name"] == pitcher_name), None)
    if not pitcher_id:
        return []

    # get statcast + compute usage
    df = statcast_pitcher("2023-01-01", str(date.today()), player_id=pitcher_id)
    df = df[df["pitch_name"].notna()]
    total = len(df)
    if total == 0:
        return []

    counts = df["pitch_name"].value_counts().to_dict()

    # return objects sorted by usage desc
    pitches = [
        {"type": name, "usage": round(cnt / total, 3), "count": int(cnt)}
        for name, cnt in sorted(counts.items(), key=lambda x: x[1], reverse=True)
    ]
    return pitches

@app.get("/api/raw/{batter_name}/{pitcher_name}/{pitch_type}")
def get_raw_data(batter_name: str, pitcher_name: str, pitch_type: str):
    start = "2023-01-01"
    end = str(date.today())

    with open("data/batters.json") as f:
        batters = json.load(f)
    with open("data/pitchers.json") as f:
        pitchers = json.load(f)

    batter_id = next((p["player_id"] for p in batters if p["name"] == batter_name), None)
    pitcher_id = next((p["player_id"] for p in pitchers if p["name"] == pitcher_name), None)

    if not batter_id or not pitcher_id:
        return {"error": "Player not found"}

    batter_df = statcast_batter(start, end, batter_id)
    pitcher_df = statcast_pitcher(start, end, pitcher_id)

    # Filter both by pitch_type
    batter_df = batter_df[batter_df["pitch_name"] == pitch_type]
    pitcher_df = pitcher_df[pitcher_df["pitch_name"] == pitch_type]

    # Drop unnecessary columns for readability
    cols = ["pitch_name", "description", "events", "bb_type", "type"]
    batter_df = batter_df[cols].replace({np.nan: None})
    pitcher_df = pitcher_df[cols].replace({np.nan: None})

    return {
        "batter_sample": len(batter_df),
        "pitcher_sample": len(pitcher_df),
        "batter_data": batter_df.to_dict(orient="records"),
        "pitcher_data": pitcher_df.to_dict(orient="records")
        # "batter_data": batter_df.head(50).to_dict(orient="records"),
        # "pitcher_data": pitcher_df.head(50).to_dict(orient="records"),
    }
