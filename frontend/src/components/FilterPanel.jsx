import { useState } from "react";
import "./FilterPanel.css";

export default function FilterPanel({ 
  searchQuery, 
  onSearchChange,
  sortBy,
  onSortChange,
  onReset
}) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="filter-panel">
      <div className="filter-row">
        <div className="search-box">
          <svg className="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none">
            <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2"/>
            <path d="M20 20L16 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
          <input
            type="text"
            placeholder="아이템 검색..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="search-input"
          />
          {searchQuery && (
            <button 
              className="search-clear" 
              onClick={() => onSearchChange("")}
              aria-label="검색어 지우기"
            >
              ✕
            </button>
          )}
        </div>

        <div className="filter-actions">
          <select 
            value={sortBy} 
            onChange={(e) => onSortChange(e.target.value)}
            className="sort-select"
          >
            <option value="price-desc">가격 높은순</option>
            <option value="price-asc">가격 낮은순</option>
            <option value="name-asc">이름순</option>
            <option value="change-desc">상승률순</option>
            <option value="change-asc">하락률순</option>
            <option value="quantity-desc">수량 많은순</option>
          </select>

          <button 
            className="filter-toggle secondary"
            onClick={() => setIsExpanded(!isExpanded)}
          >
            필터 {isExpanded ? "접기" : "펼치기"}
          </button>

          <button 
            className="filter-reset secondary"
            onClick={onReset}
          >
            초기화
          </button>
        </div>
      </div>

      {isExpanded && (
        <div className="filter-expanded">
          <div className="filter-group">
            <label className="filter-label">가격 범위</label>
            <div className="filter-range">
              <input type="number" placeholder="최소" min="0" />
              <span>~</span>
              <input type="number" placeholder="최대" />
            </div>
          </div>

          <div className="filter-group">
            <label className="filter-label">가격 변동</label>
            <div className="filter-checkboxes">
              <label className="checkbox-label">
                <input type="checkbox" />
                <span>상승 중</span>
              </label>
              <label className="checkbox-label">
                <input type="checkbox" />
                <span>하락 중</span>
              </label>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

