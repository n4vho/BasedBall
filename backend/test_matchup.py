from src.matchup_evaluator import evaluate_matchup
from src.pitcher_statcast_live import get_pitcher_pitch_usage
from src.batter_statcast_live import pitch_based_outcome
from pybaseball import playerid_lookup, statcast_batter, statcast_pitcher

start_date = "2023-01-01"
end_date = "2025-04-11"

batterFirstName, batterLastName = input("Enter the batter's name: ").split()
firstName, lastName = input("Enter the pitcher's name: ").split()

pitcher_id = playerid_lookup(lastName, firstName).iloc[0]['key_mlbam']
pitcher_df = statcast_pitcher(start_date, end_date, player_id=pitcher_id)
pitcher_profile = get_pitcher_pitch_usage(pitcher_df)


batter_id = playerid_lookup(batterLastName, batterFirstName).iloc[0]['key_mlbam']
batter_df = statcast_batter(start_date, end_date, player_id=batter_id)
batter_profile = pitch_based_outcome(batter_df)


outcome = evaluate_matchup(batter_profile, pitcher_profile)

print(f"\nMatchup prediction: {batterFirstName.upper()} {batterLastName.upper()} vs {firstName.upper()} {lastName.upper()}")
for key, val in outcome.items():
    print(f"  {key}: {val*100:.1f}%")
