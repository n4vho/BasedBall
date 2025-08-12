
from fastapi import APIRouter, Query
from pybaseball import playerid_lookup, statcast_pitcher
from src.pitcher_statcast_live import get_pitcher_pitch_usage
from datetime import date

router = APIRouter()

@router.get("/api/pitcher-profile")
def pitcher_profile(name: str = Query(..., example="Chris Bassitt")):
    try:
        first, last = name.strip().split()
        player_id = playerid_lookup(last, first).iloc[0]['key_mlbam']
        start_date = "2023-01-01"
        end_date = str(date.today())
        df = statcast_pitcher(start_date, end_date, player_id=player_id)

        profile = get_pitcher_pitch_usage(df)
        return {
            "player_id": player_id,
            "name": name,
            "profile": profile
        }
    except Exception as e:
        return {"error": str(e)}
