import { useState, useEffect } from "react";
import BatterSelect from "./components/BatterSelect.jsx";
import PitcherSelect from "./components/PitcherSelect.jsx";
import MatchupResultCard from "./components/MatchupResultCard.jsx";
import PitchTypeSelect from "./components/PitchTypeSelect";


export default function App() {
  const [batter, setBatter] = useState(null);
  const [pitcher, setPitcher] = useState(null);
  const [result, setResult] = useState(null);
  const [pitchType, setPitchType] = useState("");
  const [pitchTypes, setPitchTypes] = useState([]);

  useEffect(() => {
    if (pitcher) {
      fetch(`http://basedball.onrender.com/api/pitch-types/${pitcher}`)
        .then((res) => res.json())
        .then((data) => setPitchTypes(data));
    }
  }, [pitcher]);
  

  async function simulateMatchup(batter, pitcher) {
    const payload = {
      batter: batter,
      pitcher: pitcher,
      pitch_type: pitchType || "",
    };
  
    console.log("Sending payload:", payload); // inspect this in browser console
  
    try {
      const res = await fetch("http://basedball.onrender.com/api/matchup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
  
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Error in simulateMatchup:", err);
      alert("Failed to fetch matchup");
    }
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-800 text-white font-sans px-6 py-10">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-5xl font-extrabold text-center mb-12 tracking-tight">
          Batter vs Pitcher Matchup <span className="ml-2">⚾</span>
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
          <div>
            <h2 className="text-lg font-semibold mb-2">Select Batter</h2>
            <BatterSelect onSelect={setBatter} />
          </div>
          <div>
            <h2 className="text-lg font-semibold mb-2">Select Pitcher</h2>
            <PitcherSelect onSelect={setPitcher} />

          </div>
        </div>

        {batter && pitcher && (
          <div className="text-center space-y-4">
            <div className="flex justify-center items-center gap-4">
              <div className="flex flex-col items-center">
                <img
                  src={`https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/${batter.player_id}/headshot/67/current`}
                  alt={batter.name}
                  className="w-21 h-25 shadow-lg"
                />
                <p className="text-blue-300 mt-2">{batter.name}</p>
              </div>

              <span className="text-xl text-gray-400">vs</span>

              <div className="flex flex-col items-center">
                <img
                  src={`https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/${pitcher.player_id}/headshot/67/current`}
                  alt={pitcher.name}
                  className="w-21 h-25 shadow-lg"
                />
                <p className="text-rose-300 mt-2">{pitcher.name}</p>
              </div>
            </div>

            <PitchTypeSelect
              pitchTypes={[
                "4-Seam Fastball",
                "Sinker",
                "Slider",
                "Cutter",
                "Changeup",
                "Curveball",
                "Split-Finger",
                "Sweeper",
              ]}
              selected={pitchType}
              onSelect={setPitchType}
            />

            <button
              onClick={() => simulateMatchup(batter.name, pitcher.name)}
              className="mt-4 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 px-6 rounded shadow transition duration-200"
            >
              Pitch now!
            </button>
          </div>
        )}

        {result && (
          <MatchupResultCard
            batter={batter}
            pitcher={pitcher}
            result={result}
          />
        )}
      </div>
    </div>
  );
}