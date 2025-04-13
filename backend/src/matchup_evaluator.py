def evaluate_matchup(batter_data: dict, pitcher_data: dict) -> dict:
    outcome_totals = {
        "Strikeout%": 0.0,
        "GB%": 0.0,
        "FB%": 0.0,
        "LD%": 0.0,
        "PopUp%": 0.0
    }
    total_usage = 0.0

    for pitch_type, pstats in pitcher_data.items():
        if pitch_type not in batter_data:
            continue  # Skip if batter hasn't seen this pitch

        usage = pstats["Usage%"]
        bstats = batter_data[pitch_type]

        # Average the tendencies of both batter and pitcher
        whiff = (bstats["Whiff%"] + pstats["Whiff%"]) / 2
        gb = (bstats["GB%"] + pstats["GB%"]) / 2
        fb = (bstats["FB%"] + pstats["FB%"]) / 2
        ld = (bstats["LD%"] + pstats["LD%"]) / 2
        popup = (bstats["PopUp%"] + pstats["PopUp%"]) / 2

        # Add weighted contributions
        outcome_totals["Strikeout%"] += usage * whiff
        outcome_totals["GB%"] += usage * gb
        outcome_totals["FB%"] += usage * fb
        outcome_totals["LD%"] += usage * ld
        outcome_totals["PopUp%"] += usage * popup

        total_usage += usage

    # Normalize totals (in case usage doesn't sum to 1)
    if total_usage == 0:
        return {"error": "No overlapping pitch types"}

    for k in outcome_totals:
        outcome_totals[k] = round(outcome_totals[k] / total_usage, 3)

    outcome_totals["in_play%"] = round(1.0 - outcome_totals["Strikeout%"], 3)
    return outcome_totals
