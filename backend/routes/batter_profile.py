
from fastapi import APIRouter, Query
from pybaseball import playerid_lookup, statcast_batter
from src.batter_statcast_live import pitch_based_outcome
from datetime import date

router = APIRouter()

@router.get("/api/batter-profile")
def batter_profile(name: str = Query(..., example="Mookie Betts")):
    try:
        first, last = name.strip().split()
        player_id = playerid_lookup(last, first).iloc[0]['key_mlbam']
        start_date = "2023-01-01"
        end_date = str(date.today())
        df = statcast_batter(start_date, end_date, player_id=player_id)

        profile = pitch_based_outcome(df)
        return {
            "player_id": player_id,
            "name": name,
            "profile": profile
        }
    except Exception as e:
        return {"error": str(e)}
