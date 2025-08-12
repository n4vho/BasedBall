export default function PitchTypeSelect({ pitchTypes, selected, onSelect }) {
  // accept both new (objects) and old (strings) just in case
  const normalized = (pitchTypes || []).map((p) =>
    typeof p === "string" ? { type: p, usage: null, count: null } : p
  );

  return (
    <div className="mt-6 text-center">
      <label className="text-white font-medium mr-4">Select Pitch Type:</label>
      <select
        className="bg-gray-800 text-white px-4 py-2 rounded border border-gray-600"
        value={selected}
        onChange={(e) => onSelect(e.target.value)}
      >
        <option value="">All Pitches (Weighted)</option>
        {normalized.map((p) => (
          <option key={p.type} value={p.type}>
            {p.type}
            {p.usage != null ? ` (${(p.usage * 100).toFixed(1)}%)` : ""}
            {p.count != null ? ` • ${p.count}` : ""}
          </option>
        ))}
      </select>
    </div>
  );
}
