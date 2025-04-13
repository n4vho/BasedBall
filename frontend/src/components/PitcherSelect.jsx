import { useState, useEffect } from "react";

export default function PitcherSelect({ onSelect }) {
  const [query, setQuery] = useState("");
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    fetch("http://basedball.onrender.com/api/players/pitchers")
      .then(res => res.json())
      .then(setPlayers);
  }, []);

  const filtered = players
    .filter(p => p.name.toLowerCase().startsWith(query.toLowerCase()))
    .slice(0, 5);

  const handleSelect = (player) => {
    onSelect(player);
    setQuery(player.name);
  };

  return (
    <div className="relative">
      <input
        type="text"
        placeholder="Search pitcher..."
        className="w-full px-4 py-2 rounded bg-gray-800 text-white border border-gray-600"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      {filtered.length > 0 && (
        <ul className="absolute z-10 mt-1 bg-gray-900 border border-gray-700 rounded w-full max-h-48 overflow-y-auto">
          {filtered.map((p) => (
            <li
              key={p.player_id}
              onClick={() => handleSelect(p)}
              className="px-4 py-2 hover:bg-blue-600 cursor-pointer"
            >
              {p.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
