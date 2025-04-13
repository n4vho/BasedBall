from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.pitcher_statcast_live import get_pitcher_pitch_usage
from src.batter_statcast_live import pitch_based_outcome
from src.matchup_evaluator import evaluate_matchup
from pybaseball import playerid_lookup, statcast_pitcher, statcast_batter

app = FastAPI()

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MatchupRequest(BaseModel):
    batter: str
    pitcher: str

@app.post("/api/matchup")
def get_matchup(data: MatchupRequest):
    batter_first, batter_last = data.batter.split()
    pitcher_first, pitcher_last = data.pitcher.split()

    batter_id = playerid_lookup(batter_last, batter_first).iloc[0]['key_mlbam']
    pitcher_id = playerid_lookup(pitcher_last, pitcher_first).iloc[0]['key_mlbam']

    batter_df = statcast_batter("2023-01-01", "2025-04-11", player_id=batter_id)
    pitcher_df = statcast_pitcher("2023-01-01", "2025-04-11", player_id=pitcher_id)

    batter_data = pitch_based_outcome(batter_df)
    pitcher_data = get_pitcher_pitch_usage(pitcher_df)

    result = evaluate_matchup(batter_data, pitcher_data)
    return result
