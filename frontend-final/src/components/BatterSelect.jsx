import { useState } from "react";

const playerList = [
  "Mookie Betts",
  "Aaron Judge",
  "Mike Trout",
  "George Springer",
  "Juan Soto",
  "Ronald Acuña Jr.",
  "Shohei Ohtani",
  "Bryce Harper",
  "Freddie Freeman",
  "Vladimir Guerrero Jr."
];

export default function BatterSelect({ onSelect }) {
  const [query, setQuery] = useState("");

  const filtered = playerList.filter(name =>
    name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div>
      <label className="block text-sm text-gray-200 mb-1">Select Batter</label>
      <input
        className="w-full px-4 py-2 rounded bg-gray-800 text-white border border-gray-700 focus:outline-none"
        placeholder="Type batter name"
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
