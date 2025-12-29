import { useState, useEffect } from "react";
import "./FarmingGuide.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8001/api";

const CATEGORY_LABELS = {
  mapping: "맵핑",
  boss: "보스",
  league: "리그 컨텐츠",
  crafting: "제작",
  trading: "거래",
  mechanic: "메카닉",
};

const DIFFICULTY_LABELS = {
  beginner: "초보자",
  intermediate: "중급",
  advanced: "고급",
  expert: "전문가",
};

const DIFFICULTY_COLORS = {
  beginner: "#4ade80",
  intermediate: "#60a5fa",
  advanced: "#f472b6",
  expert: "#f87171",
};

// 화폐 아이콘
const DIVINE_ICON = "https://web.poecdn.com//gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvQ3VycmVuY3lNb2RWYWx1ZXMiLCJzY2FsZSI6MSwicmVhbG0iOiJwb2UyIn1d/2986e220b3/CurrencyModValues.png";

export default function FarmingGuide() {
  const [methods, setMethods] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedMethod, setSelectedMethod] = useState(null);
  const [filterCategory, setFilterCategory] = useState("");
  const [filterDifficulty, setFilterDifficulty] = useState("");

  useEffect(() => {
    fetchMethods();
  }, [filterCategory, filterDifficulty]);

  const fetchMethods = async () => {
    setLoading(true);
    setError(null);

    try {
      let url = `${API_URL}/farming-methods/`;
      const params = new URLSearchParams();
      if (filterCategory) params.append("category", filterCategory);
      if (filterDifficulty) params.append("difficulty", filterDifficulty);
      if (params.toString()) url += `?${params.toString()}`;

      const response = await fetch(url);
      if (!response.ok) throw new Error("데이터를 불러오지 못했습니다");

      const data = await response.json();
      setMethods(data.methods || []);
    } catch (err) {
      setError(err.message);
      setMethods([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchMethodDetail = async (slug) => {
    try {
      const response = await fetch(`${API_URL}/farming-methods/${slug}/`);
      if (!response.ok) throw new Error("상세 정보를 불러오지 못했습니다");
      const data = await response.json();
      setSelectedMethod(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const formatProfit = (min, max) => {
    if (!min && !max) return "-";
    if (min === max) return `${min} div/h`;
    return `${min}-${max} div/h`;
  };

  return (
    <div className="farming-guide">
      <div className="guide-header">
        <h1>🎮 파밍 가이드</h1>
        <p className="guide-subtitle">
          바알의 운명 리그 기준 · 최신 파밍 전략
        </p>
      </div>

      {/* 필터 */}
      <div className="guide-filters">
        <select
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value)}
          className="filter-select"
        >
          <option value="">전체 카테고리</option>
          {Object.entries(CATEGORY_LABELS).map(([key, label]) => (
            <option key={key} value={key}>
              {label}
            </option>
          ))}
        </select>

        <select
          value={filterDifficulty}
          onChange={(e) => setFilterDifficulty(e.target.value)}
          className="filter-select"
        >
          <option value="">전체 난이도</option>
          {Object.entries(DIFFICULTY_LABELS).map(([key, label]) => (
            <option key={key} value={key}>
              {label}
            </option>
          ))}
        </select>
      </div>

      {/* 에러 */}
      {error && (
        <div className="guide-error">
          <p>❌ {error}</p>
          <button onClick={fetchMethods}>다시 시도</button>
        </div>
      )}

      {/* 로딩 */}
      {loading && (
        <div className="guide-loading">
          <div className="spinner"></div>
          <p>파밍 가이드를 불러오는 중...</p>
        </div>
      )}

      {/* 메인 컨텐츠 */}
      {!loading && !error && (
        <div className="guide-content">
          {/* 파밍 방법 목록 */}
          <div className="methods-grid">
            {methods.map((method) => (
              <div
                key={method.id}
                className={`method-card ${selectedMethod?.slug === method.slug ? "active" : ""}`}
                onClick={() => fetchMethodDetail(method.slug)}
              >
                <div className="method-header">
                  {method.icon?.startsWith("http") ? (
                    <img src={method.icon} alt="" className="method-icon-img" />
                  ) : (
                    <span className="method-icon">{method.icon}</span>
                  )}
                  <div className="method-badges">
                    <span
                      className="difficulty-badge"
                      style={{ backgroundColor: DIFFICULTY_COLORS[method.difficulty] }}
                    >
                      {DIFFICULTY_LABELS[method.difficulty]}
                    </span>
                    {method.is_league_specific && (
                      <span className="league-badge">리그 한정</span>
                    )}
                  </div>
                </div>

                <h3 className="method-title">{method.name_ko}</h3>
                <p className="method-name-en">{method.name}</p>
                <p className="method-summary">{method.summary}</p>

                <div className="method-stats">
                  <div className="stat">
                    <span className="stat-label">예상 수익</span>
                    <span className="stat-value profit">
                      <img src={DIVINE_ICON} alt="Divine" className="currency-icon-sm" />
                      {method.estimated_profit_min}-{method.estimated_profit_max}/h
                    </span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">초기 투자</span>
                    <span className="stat-value investment">
                      <img src={DIVINE_ICON} alt="Divine" className="currency-icon-sm" />
                      {method.investment_required}
                    </span>
                  </div>
                </div>

                <div className="method-footer">
                  <span className="method-category">
                    {CATEGORY_LABELS[method.category] || method.category}
                  </span>
                  {method.creator_name && (
                    <span className="creator-badge">
                      🎬 {method.creator_name}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* 상세 정보 모달/패널 */}
          {selectedMethod && (
            <div className="method-detail-overlay" onClick={() => setSelectedMethod(null)}>
              <div className="method-detail" onClick={(e) => e.stopPropagation()}>
                <button className="close-btn" onClick={() => setSelectedMethod(null)}>
                  ✕
                </button>

                <div className="detail-header">
                  {selectedMethod.icon?.startsWith("http") ? (
                    <img src={selectedMethod.icon} alt="" className="detail-icon-img" />
                  ) : (
                    <span className="detail-icon">{selectedMethod.icon}</span>
                  )}
                  <div>
                    <h2>{selectedMethod.name_ko}</h2>
                    <p className="detail-name-en">{selectedMethod.name}</p>
                  </div>
                </div>

                <div className="detail-badges">
                  <span
                    className="difficulty-badge"
                    style={{ backgroundColor: DIFFICULTY_COLORS[selectedMethod.difficulty] }}
                  >
                    {DIFFICULTY_LABELS[selectedMethod.difficulty]}
                  </span>
                  <span className="category-badge">
                    {CATEGORY_LABELS[selectedMethod.category]}
                  </span>
                  {selectedMethod.is_league_specific && (
                    <span className="league-badge">🏛️ {selectedMethod.league} 한정</span>
                  )}
                </div>

                <div className="detail-profit">
                  <div className="profit-item">
                    <span className="profit-label">예상 수익 (시간당)</span>
                    <span className="profit-value">
                      <img src={DIVINE_ICON} alt="Divine" className="currency-icon-lg" />
                      {selectedMethod.estimated_profit_min}-{selectedMethod.estimated_profit_max}
                    </span>
                  </div>
                  <div className="profit-item">
                    <span className="profit-label">초기 투자</span>
                    <span className="profit-value investment">
                      <img src={DIVINE_ICON} alt="Divine" className="currency-icon-lg" />
                      {selectedMethod.investment_required}
                    </span>
                  </div>
                </div>

                <div className="detail-section">
                  <h3>📋 요약</h3>
                  <p>{selectedMethod.summary}</p>
                </div>

                <div className="detail-section">
                  <h3>📖 상세 설명</h3>
                  <div className="description-content">
                    {selectedMethod.description.split("\n").map((line, i) => (
                      <p key={i}>{line}</p>
                    ))}
                  </div>
                </div>

                {selectedMethod.requirements?.length > 0 && (
                  <div className="detail-section">
                    <h3>✅ 필요 조건</h3>
                    <ul className="requirements-list">
                      {selectedMethod.requirements.map((req, i) => (
                        <li key={i}>{req}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {selectedMethod.recommended_items?.length > 0 && (
                  <div className="detail-section">
                    <h3>🎒 추천 아이템</h3>
                    <div className="items-grid">
                      {selectedMethod.recommended_items.map((item, i) => (
                        <div key={i} className="recommended-item">
                          <span className="item-name">{item.name_ko || item.name}</span>
                          <span className="item-desc">{item.description}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {selectedMethod.steps?.length > 0 && (
                  <div className="detail-section">
                    <h3>📝 진행 단계</h3>
                    <ol className="steps-list">
                      {selectedMethod.steps.map((step, i) => (
                        <li key={i}>
                          <strong>{step.title}</strong>
                          <p>{step.description}</p>
                        </li>
                      ))}
                    </ol>
                  </div>
                )}

                {selectedMethod.tips?.length > 0 && (
                  <div className="detail-section">
                    <h3>💡 팁</h3>
                    <ul className="tips-list">
                      {selectedMethod.tips.map((tip, i) => (
                        <li key={i}>{tip}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* 크리에이터 정보 */}
                {selectedMethod.creator_name && (
                  <div className="detail-section creator-section">
                    <h3>🎬 크리에이터</h3>
                    <div className="creator-info">
                      <span className="creator-name">{selectedMethod.creator_name}</span>
                      {selectedMethod.creator_url && (
                        <a 
                          href={selectedMethod.creator_url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="creator-link"
                        >
                          채널 방문 →
                        </a>
                      )}
                    </div>
                  </div>
                )}

                {selectedMethod.source_url && (
                  <div className="detail-source">
                    <a href={selectedMethod.source_url} target="_blank" rel="noopener noreferrer">
                      📎 출처 보기
                    </a>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

