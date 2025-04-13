import pandas as pd

def get_pitcher_pitch_usage(df):
    """
    Returns a dictionary like:
    {
        "Slider": {
            "usage%": 0.28,
            "whiff%": 0.34,
            "xBA": 0.210,
            "xSLG": 0.390,
            ...
        },
        ...
    }
    """
    if df.empty:
        print(f"⚠️ No data for {first_name} {last_name} between {start_date} and {end_date}")
        return {}

    df = df[df["pitch_name"].notna()]

    total_pitches = len(df)
    grouped = df.groupby("pitch_name")

    result = {}

    for pitch, group in grouped:
        usage = len(group) / total_pitches
        contact_df = group[group["bb_type"].notna()]
        total_contact = len(contact_df)
        
        is_whiff = group["description"].isin(["swinging_strike", "swinging_strike_blocked"])
        avg_xba = group["estimated_ba_using_speedangle"].mean()
        avg_xslg = group["estimated_slg_using_speedangle"].mean()

        gb_pct = (contact_df["bb_type"] == "ground_ball").sum() / total_contact if total_contact else 0.0
        fb_pct = (contact_df["bb_type"] == "fly_ball").sum() / total_contact if total_contact else 0.0
        ld_pct = (contact_df["bb_type"] == "line_drive").sum() / total_contact if total_contact else 0.0
        popup_pct = (contact_df["bb_type"] == "popup").sum() / total_contact if total_contact else 0.0

        result[pitch] = {
            "Usage%": round(usage, 3),
            "Whiff%": round(is_whiff.sum() / len(group), 3) if len(group) > 0 else 0.0,
            "xBA": round(avg_xba, 3) if not pd.isna(avg_xba) else 0.0,
            "xSLG": round(avg_xslg, 3) if not pd.isna(avg_xslg) else 0.0,
            "GB%": round(gb_pct, 3),
            "FB%": round(fb_pct, 3),
            "LD%": round(ld_pct, 3),
            "PopUp%": round(popup_pct, 3),
            "Total pitches": len(group)
        }


    return result
