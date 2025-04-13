from src.analyzer import load_data, analyze_matchup

def run():
    batters, pitchers = load_data()

    print("Available Batters: Aaron Judge, Shohei Ohtani")
    batter = input("Select batter: ")

    print("Available Pitchers: Roki Sasaki, Jacob deGrom")
    pitcher = input("Select pitcher: ")

    print("Available Pitch Types: slider, splitter, four-seamer")
    pitch = input("Select pitch type: ")

    result = analyze_matchup(batter, pitcher, pitch, batters, pitchers)
    if isinstance(result, str):
        print(result)
    else:
        print(f"\nMatchup Analysis for {batter} vs {pitcher} ({pitch}):")
        print(f"- Batter AVG vs {pitch}: {result['batter_avg']}")
        print(f"- Slugging: {result['slugging']}")
        print(f"- Home Run Rate: {result['home_run_rate']}")
        print(f"- Pitch Usage Rate: {result['pitch_usage']}")
        print("\nEstimated Outcome Probabilities:")
        for outcome, prob in result['outcomes'].items():
            print(f"  • {outcome.capitalize()}: {prob*100:.1f}%")


