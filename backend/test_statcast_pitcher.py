from src.pitcher_statcast_live import *
from pybaseball import statcast_pitcher, playerid_lookup

start_date = "2023-01-01"
end_date = "2025-04-11"

firstName, lastName = input("Enter the pitcher's name: ").split()

pitcher_id = playerid_lookup(lastName, firstName).iloc[0]['key_mlbam']
df = statcast_pitcher(start_date, end_date, player_id=pitcher_id)

pitcher_stats = get_pitcher_pitch_usage(df)

print(f"\n{firstName} {lastName}'s performance from {start_date} to {end_date}:\n")
for pitch, stats in pitcher_stats.items():
    print(f"{pitch}:")
    for k, v in stats.items():
        print(f"    {k}: {v}")
