import { useState } from "react";

export default function SearchBar({ value, onChange, placeholder = "아이템 검색..." }) {
  const [focused, setFocused] = useState(false);

  return (
    <div className={`search-bar ${focused ? "focused" : ""}`}>
      <span className="search-bar__icon">🔍</span>
      <input
        type="text"
        className="search-bar__input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        placeholder={placeholder}
      />
      {value && (
        <button 
          className="search-bar__clear" 
          onClick={() => onChange("")}
          type="button"
        >
          ✕
        </button>
      )}
    </div>
  );
}

