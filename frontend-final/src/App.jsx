/*
This file is the main entry point for your cleaned-up, styled, fully working
batter vs pitcher matchup app. All Tailwind, Vite, and React config has been fixed.
*/

import { useState } from "react";
import BatterSelect from "./components/BatterSelect";
import PitcherSelect from "./components/PitcherSelect";
import MatchupResultCard from "./components/MatchupResultCard";

export default function App() {
  const [batter, setBatter] = useState(null);
  const [pitcher, setPitcher] = useState(null);
  const [result, setResult] = useState(null);

  async function simulateMatchup(batter, pitcher) {
    try {
      const response = await fetch("http://localhost:8000/api/matchup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ batter, pitcher }),
      });

      if (!response.ok) throw new Error("API error");

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error("Matchup error:", err);
      alert("Failed to fetch matchup results.");
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white p-8">
      <h1 className="text-4xl font-extrabold mb-10 text-center tracking-tight">
        Batter vs Pitcher Matchup ⚾
      </h1>

      <div className="max-w-2xl mx-auto space-y-8">
        <BatterSelect onSelect={setBatter} />
        <PitcherSelect onSelect={setPitcher} />

        {batter && pitcher && (
          <>
            <div className="text-center mt-6">
              <p className="text-xl">
                👤 <span className="font-bold text-blue-400">{batter}</span>
              </p>
              <p className="text-xl">
                🧢 vs <span className="font-bold text-rose-400">{pitcher}</span>
              </p>
            </div>

            <div className="text-center">
              <button
                className="mt-4 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-6 py-2 rounded-lg border border-indigo-400 shadow-md transition-all duration-200"
                onClick={() => simulateMatchup(batter, pitcher)}
              >
                Compare
              </button>
            </div>

            <MatchupResultCard
              batter={batter}
              pitcher={pitcher}
              result={result}
            />
          </>
        )}
      </div>
    </div>
  );
}
