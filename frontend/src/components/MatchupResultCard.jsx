export default function MatchupResultCard({ batter, pitcher, result }) {
    if (!result) return null;
  
    const labelMap = {
      strikeout: "Strikeout%",
      ground_ball: "GB%",
      fly_ball: "FB%",
      line_drive: "LD%",
      popup: "PopUp%",
      in_play: "In Play%"
    };
  
    const getColor = (key) => {
      switch (key) {
        case "strikeout":
          return "text-red-400";
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
  
    return (
      <div className="bg-gray-800 text-white p-8 rounded-lg shadow-xl mt-10 max-w-xl mx-auto border border-gray-700">
        <h2 className="text-2xl font-semibold mb-6 text-center">
          Matchup Result: <span className="text-blue-400">{batter}</span> vs <span className="text-rose-400">{pitcher}</span>
        </h2>
        <div className="space-y-4 text-lg">
          {Object.entries(result).map(([key, value]) => (
            <div key={key} className="flex justify-between">
              <span className={`${getColor(key)} font-medium`}>{labelMap[key] || key}</span>
              <span className={`${getColor(key)} font-semibold`}>
                {(value * 100).toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  }
  