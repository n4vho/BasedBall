from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from datetime import date
from dateutil.relativedelta import relativedelta
from pybaseball import statcast_batter, statcast_pitcher, playerid_reverse_lookup, playerid_reverse_lookup
from collections import defaultdict


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define Pydantic model BEFORE using it
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
    outcome_counts = defaultdict(int)
    total = 0

    for _, row in df.iterrows():
        des = str(row.get("description", "")).lower()
        if "strike" in des and "swinging" in des:
            outcome_counts["strikeout"] += 1
        elif row.get("events") == "strikeout":
            outcome_counts["strikeout"] += 1
        elif row.get("bb_type") == "ground_ball":
            outcome_counts["ground_ball"] += 1
        elif row.get("bb_type") == "line_drive":
            outcome_counts["line_drive"] += 1
        elif row.get("bb_type") == "fly_ball":
            outcome_counts["fly_ball"] += 1
        elif row.get("bb_type") == "popup":
            outcome_counts["popup"] += 1
        elif row.get("type") == "X":
            outcome_counts["in_play"] += 1

        total += 1

    return {k: v / total for k, v in outcome_counts.items()} if total > 0 else {}

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

@app.post("/api/matchup")
def evaluate_matchup(req: MatchupRequest):
    print("REQ:", req.batter, req.pitcher, req.pitch_type)
    print(f"[*] Simulating: {req.batter} vs {req.pitcher}")
    start = "2023-01-01"
    end = str(date.today())

    batter_id = next((p["player_id"] for p in json.load(open("data/batters.json")) if p["name"] == req.batter), None)
    pitcher_id = next((p["player_id"] for p in json.load(open("data/pitchers.json")) if p["name"] == req.pitcher), None)

    if not batter_id or not pitcher_id:
        return {"error": "Player ID not found"}

    # Fetch real statcast data
    batter_df = statcast_batter(start, end, batter_id)
    pitcher_df = statcast_pitcher(start, end, pitcher_id)

    batter_by_pitch = group_by_pitch(batter_df)
    pitcher_by_pitch = group_by_pitch(pitcher_df)

    total_pitch_usage = sum(v["usage"] for v in pitcher_by_pitch.values())
    if total_pitch_usage == 0:
        return {"error": "Pitcher has no pitch data"}

    # Weighted outcome computation
    combined = defaultdict(float)
    print("Pitcher pitch types:", list(pitcher_by_pitch.keys()))
    print("Batter pitch types:", list(batter_by_pitch.keys()))

    for pitch, pdata in pitcher_by_pitch.items():
        if pitch not in batter_by_pitch:
            continue
        # If user selected a pitch, filter to only that
        if req.pitch_type and pitch != req.pitch_type:
            continue


        batter_outcomes = batter_by_pitch[pitch]["outcomes"]
        usage_weight = pdata["usage"] / total_pitch_usage

        for outcome, val in batter_outcomes.items():
            combined[outcome] += val * usage_weight

    # Normalize total outcome percentages
    total = sum(combined.values())
    if total == 0:
        return {"error": "No shared pitch data"}

    for k in combined:
        combined[k] = round(combined[k], 4)

    # Add in_play if not covered
    combined["in_play"] = round(1.0 - combined.get("strikeout", 0.0), 4)

    return combined

@app.get("/api/pitch-types/{pitcher_name}")
def get_pitch_types(pitcher_name: str):
    pitcher_id = next((p["player_id"] for p in json.load(open("data/pitchers.json")) if p["name"] == pitcher_name), None)
    if not pitcher_id:
        return []

    df = statcast_pitcher("2023-01-01", str(date.today()), player_id=pitcher_id)
    pitch_types = df["pitch_type"].dropna().unique().tolist()
    return sorted(pitch_types)
