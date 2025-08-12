import { useEffect, useState, useRef } from "react";

function normalize(str) {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

export default function BatterSelect({ onSelect }) {
  const [query, setQuery] = useState("");
  const [batters, setBatters] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    // fetch("https://basedball.onrender.com/api/players/batters")
    fetch("/api/players/batters")
      .then((res) => res.json())
      .then((data) => {
        setBatters(data);
        setFiltered(data);
      });
  }, []);

  useEffect(() => {
    const search = normalize(query);
    setFiltered(
      batters.filter((b) => normalize(b.name).includes(search)).slice(0, 5)
    );
  }, [query, batters]);

  function handleSelect(batter) {
    setQuery(batter.name);
    setShowDropdown(false);
    onSelect(batter);
  }

  useEffect(() => {
    function handleClickOutside(e) {
      if (!inputRef.current.contains(e.target)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={inputRef}>
      <input
        className="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:outline-none"
        placeholder="Search batter..."
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setShowDropdown(true);
        }}
        onFocus={() => setShowDropdown(true)}
      />
      {showDropdown && (
        <ul className="absolute z-10 w-full bg-gray-800 border border-gray-600 rounded mt-1 max-h-40 overflow-y-auto">
          {filtered.map((batter) => (
            <li
              key={batter.player_id}
              className="p-2 hover:bg-gray-700 cursor-pointer"
              onClick={() => handleSelect(batter)}
            >
              {batter.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
