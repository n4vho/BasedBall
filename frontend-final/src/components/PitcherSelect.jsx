import { useState } from "react";

const pitcherList = [
  "Chris Bassitt",
  "Shohei Ohtani",
  "Jacob deGrom",
  "Gerrit Cole",
  "Zack Wheeler",
  "Max Scherzer",
  "Sandy Alcantara",
  "Yu Darvish",
  "Corbin Burnes",
  "Logan Webb"
];

export default function PitcherSelect({ onSelect }) {
  const [query, setQuery] = useState("");

  const filtered = pitcherList.filter(name =>
    name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div>
      <label className="block text-sm text-gray-200 mb-1">Select Pitcher</label>
      <input
        className="w-full px-4 py-2 rounded bg-gray-800 text-white border border-gray-700 focus:outline-none"
        placeholder="Type pitcher name"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && filtered.length > 0) {
            onSelect(filtered[0]);
            setQuery(filtered[0]);
          }
        }}
      />
      <ul className="mt-2 max-h-48 overflow-auto rounded border border-gray-600 bg-gray-900 text-sm">
        {filtered.map((name) => (
          <li
            key={name}
            className="px-4 py-2 hover:bg-gray-700 cursor-pointer"
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
