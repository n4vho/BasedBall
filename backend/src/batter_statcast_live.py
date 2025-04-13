import pandas as pd

def get_batter_statcast_data(df):
    """
    Get statcast data for a batter between start_date and end_date.
    Returns pitch-type breakdown with AVG, SLG, HR%.
    """
    
    if df.empty:
        print(f"No data found for {first_name} {last_name} between {start_date} and {end_date}")
        return {}

    df = df[df["events"].notna() & df["pitch_name"].notna()]

    result = {}
    grouped = df.groupby("pitch_name")


    for pitch, group in grouped:
        total = len(group)
        hits = group["events"].isin(["single", "double", "triple", "home_run"]).sum()
        home_runs = (group["events"] == "home_run").sum()
        slugging_total = (
            (group["events"] == "single").sum() +
            (group["events"] == "double").sum() * 2 +
            (group["events"] == "triple").sum() * 3 +
            home_runs * 4
        )

        ba = hits / total if total else 0
        slg = slugging_total / total if total else 0
        hr_rate = home_runs / total if total else 0

        result[pitch] = {
            "batting_avg": float(round(ba, 3)),
            "slugging": float(round(slg, 3)),
            "home_run_rate": float(round(hr_rate, 3)),
            "total_pitches_seen": int(total)
        }

    return result

def get_swing_and_contact(df):
    result = {}

    is_swing = df["description"].isin([
        "foul", "foul_tip", "hit_into_play",
        "swinging_strike", "swinging_strike_blocked"
    ])
    
    is_whiff = df["description"].isin([
        "swinging_strike", "swinging_strike_blocked"
    ])
    
    result["Swing%"] = float(round(is_swing.sum() / len(df), 3)) if len(df) > 0 else 0.0
    result["Whiff%"] = float(round(is_whiff.sum() / is_swing.sum(), 3)) if is_swing.sum() > 0 else 0.0


    contact_df = df[df["bb_type"].notna()]
    total_contact = len(contact_df)

    if total_contact > 0:
        result["GB%"] = float(round((contact_df["bb_type"] == "ground_ball").sum() / total_contact, 3))
        result["FB%"] = float(round((contact_df["bb_type"] == "fly_ball").sum() / total_contact, 3))
        result["LD%"] = float(round((contact_df["bb_type"] == "line_drive").sum() / total_contact, 3))
        result["PopUp%"] = float(round((contact_df["bb_type"] == "popup").sum() / total_contact, 3))
    else:
        result.update({"GB%": 0.0, "FB%": 0.0, "LD%": 0.0, "PopUp%": 0.0})

    return result

def pitch_based_outcome(df):
    """
    Returns a dictionary like:
    {
        "Slider": {
            "swing%": 0.4,
            "whiff%": 0.2,
            "gb%": 0.5,
            ...
        },
        ...
    }
    """

    result = {}
    df = df[df["pitch_name"].notna()]

    grouped = df.groupby("pitch_name")

    for pitch, group in grouped:
        pitch_stats = get_swing_and_contact(group)

        result[pitch] = pitch_stats

    return result