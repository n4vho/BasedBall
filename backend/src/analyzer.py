import pandas as pd

def load_data():
    batters = pd.read_csv("data/sample_batter.csv")
    pitchers = pd.read_csv("data/sample_pitcher.csv")
    return batters, pitchers

def analyze_matchup(batter_name, pitcher_name, pitch_type, batters, pitchers):
    # Get batter's stats
    batter_row = batters[(batters['batter'] == batter_name) & (batters['pitch_type'] == pitch_type)]
    pitcher_row = pitchers[(pitchers['pitcher'] == pitcher_name) & (pitchers['pitch_type'] == pitch_type)]
    
    if batter_row.empty or pitcher_row.empty:
        return "Matchup data not available."
    
    ba = batter_row.iloc[0]['batting_avg']
    slg = batter_row.iloc[0]['slugging']
    hr_rate = batter_row.iloc[0]['home_run_rate']
    usage = pitcher_row.iloc[0]['usage_rate']
    
    outcome_probs = estimate_outcomes(ba, slg, hr_rate)

    return {
        "batter_avg": ba,
        "slugging": slg,
        "home_run_rate": hr_rate,
        "pitch_usage": usage,
        "outcomes": outcome_probs
    }

def estimate_outcomes(ba, slg, hr_rate):
    walk_rate = 0.08
    hit_rate = ba
    remaining_hits = hit_rate - hr_rate

    # crude estimate using SLG to guess power
    single_rate = remaining_hits * 0.75
    double_rate = remaining_hits * 0.20
    triple_rate = remaining_hits * 0.05

    out_rate = 1 - (walk_rate + hr_rate + single_rate + double_rate + triple_rate)

    return {
        "home_run": round(hr_rate, 3),
        "triple": round(triple_rate, 3),
        "double": round(double_rate, 3),
        "single": round(single_rate, 3),
        "walk": round(walk_rate, 3),
        "out": round(out_rate, 3),
    }

