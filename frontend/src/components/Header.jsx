import { useState } from "react";
import "./Header.css";

export default function Header({ currentLeague, onLeagueChange, leagues }) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-brand">
          <h1 className="header-title">PoE2 파밍 가이드</h1>
          <span className="header-subtitle">Farming Recommender</span>
        </div>

        <nav className="header-nav">
          <div className="league-selector">
            <button
              className="league-button"
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            >
              <span className="league-label">리그</span>
              <span className="league-value">{currentLeague}</span>
              <svg
                className={`league-arrow ${isDropdownOpen ? "open" : ""}`}
                width="12"
                height="12"
                viewBox="0 0 12 12"
              >
                <path
                  d="M2 4L6 8L10 4"
                  stroke="currentColor"
                  strokeWidth="2"
                  fill="none"
                />
              </svg>
            </button>
            {isDropdownOpen && leagues && (
              <div className="league-dropdown">
                {leagues.map((league) => (
                  <button
                    key={league.value}
                    className={`league-option ${
                      league.value === currentLeague ? "active" : ""
                    }`}
                    onClick={() => {
                      onLeagueChange(league.value);
                      setIsDropdownOpen(false);
                    }}
                  >
                    <span>{league.value}</span>
                    {league.divinePrice && (
                      <span className="league-divine">
                        ⬥ {Math.round(league.divinePrice)}
                      </span>
                    )}
                  </button>
                ))}
              </div>
            )}
          </div>
        </nav>
      </div>
    </header>
  );
}

