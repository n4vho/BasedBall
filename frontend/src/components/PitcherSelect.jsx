import { useEffect, useState, useRef } from "react";

function normalize(str) {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

export default function PitcherSelect({ onSelect }) {
  const [query, setQuery] = useState("");
  const [pitchers, setPitchers] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const wrapperRef = useRef(null);

  useEffect(() => {
    fetch("https://basedball.onrender.com/api/players/pitchers")
      .then((res) => res.json())
      .then((data) => {
        setPitchers(data);
        setFiltered(data);
      });
  }, []);

  useEffect(() => {
    const search = normalize(query);
    setFiltered(
      pitchers
        .filter((p) => normalize(p.name).includes(search))
        .slice(0, 6)
    );
  }, [query, pitchers]);

  useEffect(() => {
    function handleClickOutside(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  function handleSelect(pitcher) {
    setQuery(pitcher.name);
    setShowDropdown(false);
    onSelect(pitcher);
  }

  return (
    <div className="relative" ref={wrapperRef}>
      <input
        type="text"
        placeholder="Search pitcher..."
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setShowDropdown(true);
        }}
        onFocus={() => setShowDropdown(true)}
        className="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:outline-none"
      />
      {showDropdown && filtered.length > 0 && (
        <ul className="absolute z-10 w-full bg-gray-800 border border-gray-600 rounded mt-1 max-h-48 overflow-y-auto">
          {filtered.map((pitcher) => (
            <li
              key={pitcher.player_id}
              className="p-2 hover:bg-gray-700 cursor-pointer"
              onClick={() => handleSelect(pitcher)}
            >
              {pitcher.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
