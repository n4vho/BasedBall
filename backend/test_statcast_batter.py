from src.batter_statcast_live import *
from pybaseball import statcast_batter, playerid_lookup
# Choose a time range (e.g., last 7 days)
start_date = "2023-01-01"
end_date = "2025-04-11"

firstName, lastName = input("Enter the batter's name: ").split()

batter_id = playerid_lookup(lastName, firstName).iloc[0]['key_mlbam']
df = statcast_batter(start_date, end_date, player_id=batter_id)

swing_stats = get_swing_and_contact(df)
pitch_type_stats = get_batter_statcast_data(df)
pitch_outcomes = pitch_based_outcome(df)

print(f"\n{firstName} {lastName}'s performance from {start_date} to {end_date}:\n")
for pitch_type, vals in pitch_outcomes.items():
    print(f"{pitch_type}: ")
    print(f"\tSwing%: ", vals['swing%'])
    print(f"\tWhiff%: ", vals['whiff%'])
    print(f"\tGB%: ", vals['gb%'])
    print(f"\tFB%: ", vals['fb%'])
    print(f"\tLD%: ", vals['ld%'])
    print(f"\tPopUp%: ", vals['popup%'])

# print(swing_stats)
