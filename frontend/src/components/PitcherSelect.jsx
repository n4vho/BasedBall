import { useState } from "react";

const pitcherList = [
  "Chris Bassitt",
  "Gerrit Cole",
  "Jacob deGrom",
  "Shohei Ohtani",
  "Zack Wheeler",
  "Max Scherzer",
  "Logan Webb",
  "Justin Verlander",
  "Sandy Alcantara",
  "Corbin Burnes"
];

export default function PitcherSelect({ onSelect }) {
  const [query, setQuery] = useState("");

  const filtered = pitcherList.filter(name =>
    name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="mb-6">
      <label className="block text-sm text-gray-200 mb-2">Select Pitcher</label>
      <input
        type="text"
        placeholder="Type a name..."
        className="w-full px-4 py-2 rounded bg-gray-800 text-white border border-gray-700 focus:outline-none"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
            if (e.key === "Enter" && filtered.length > 0) {
              onSelect(filtered[0]);
              setQuery(filtered[0]);
            }
          }}
        
      />
      <ul className="mt-2 bg-gray-900 border border-gray-700 rounded max-h-48 overflow-auto">
        {filtered.map((name) => (
          <li
            key={name}
            className="px-4 py-2 hover:bg-gray-700 cursor-pointer text-white"
            onClick={() => {
              onSelect(name);
              setQuery(name);
            }}
          >
            {name}
          </li>
        ))}
      </ul>
    </div>
  );
}
