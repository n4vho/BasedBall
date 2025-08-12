export default function MatchupResultCard({ batter, pitcher, result }) {
  if (!result) return null;

  // nice labels
  const labelMap = {
    swinging_strike: "Swing & Miss%",
    called_strike: "Called Strike%",
    foul: "Foul%",
    ball: "Ball%",
    ground_ball: "GB%",
    fly_ball: "FB%",
    line_drive: "LD%",
    popup: "PopUp%",
    in_play: "In Play%",
  };

  // visual order: pitch result first, then contact mix
  const order = [
    "swinging_strike",
    "called_strike",
    "foul",
    "ball",
    "ground_ball",
    "fly_ball",
    "line_drive",
    "popup",
    "in_play",
  ];

  const getColor = (key) => {
    switch (key) {
      case "swinging_strike":
        return "text-red-400";
      case "called_strike":
        return "text-yellow-300";
      case "foul":
        return "text-blue-300";
      case "ball":
        return "text-gray-300";
      case "ground_ball":
        return "text-yellow-300";
      case "fly_ball":
        return "text-blue-300";
      case "line_drive":
        return "text-green-300";
      case "popup":
        return "text-purple-300";
      case "in_play":
        return "text-white";
      default:
        return "text-gray-200";
    }
  };

  // only show keys that exist in the result
  const keysToShow = order.filter((k) => k in result && typeof result[k] === "number");

  return (
    <div className="bg-gray-800 text-white p-8 rounded-lg shadow-xl mt-10 max-w-xl mx-auto border border-gray-700">
      <h2 className="text-2xl font-semibold mb-6 text-center">
        Matchup Result: <span className="text-blue-400">{batter.name}</span> vs{" "}
        <span className="text-rose-400">{pitcher.name}</span>
      </h2>

      <div className="space-y-4 text-lg">
        {keysToShow.map((key) => (
          <div key={key} className="flex justify-between">
            <span className={`${getColor(key)} font-medium`}>{labelMap[key] || key}</span>
            <span className={`${getColor(key)} font-semibold`}>
              {(result[key] * 100).toFixed(1)}%
            </span>
          </div>
        ))}
      </div>

      {/* optional note from backend (sample sizes etc.) */}
      {"note" in result && result.note && (
        <p className="text-sm text-gray-400 italic mt-4">{result.note}</p>
      )}

      {/* optional freshness line if you expose /api/league-averages and store computed_on in result */}
      {"league_updated" in result && result.league_updated && (
        <p className="text-xs text-gray-500 mt-1">
          League baselines updated: {result.league_updated}
        </p>
      )}
    </div>
  );
}
