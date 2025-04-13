export default function PitchTypeSelect({ pitchTypes, selected, onSelect }) {
    return (
      <div className="mt-6 text-center">
        <label className="text-white font-medium mr-4">Select Pitch Type:</label>
        <select
          className="bg-gray-800 text-white px-4 py-2 rounded border border-gray-600"
          value={selected}
          onChange={(e) => onSelect(e.target.value)}
        >
          <option value="">All Pitches (Weighted)</option>
          {pitchTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>
    );
  }
  