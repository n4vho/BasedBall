import pandas as pd

def load_pitcher_usage(filepath: str, pitcher_name: str) -> dict:
    """
    Given a Statcast CSV and pitcher name, returns pitch usage statistics:
    {
        'Slider': {
            'count': 120,
            'avg_velocity': 84.5,
            'usage_rate': 0.32
        },
        ...
    }
    """
    df = pd.read_csv(filepath, low_memory=False)
    print(df.columns)
    df = df[df["player_name"] == pitcher_name]
    df = df[df["pitch_name"].notna()]

    total_pitches = len(df)
    if total_pitches == 0:
        return {}
    

    grouped = df.groupby("pitch_name")
    result = {}

    for pitch_name, group in grouped:
        count = len(group)
        avg_velocity = group["release_speed"].mean()
        usage = count / total_pitches

        result[pitch_name] = {
            "count": count,
            "avg_velocity": round(avg_velocity, 1),
            "usage_rate": round(usage, 3)
        }

    return result
