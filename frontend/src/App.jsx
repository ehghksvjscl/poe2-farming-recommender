import { useState } from "react";
import "./index.css";
import Header from "./components/Header";
import FarmingForm from "./components/FarmingForm";
import RecommendationCard from "./components/RecommendationCard";
import { useLeagues } from "./hooks/useMarketData";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8001/api";

const DEFAULT_LEAGUE = "Fate of the Vaal";

export default function App() {
  const [currentLeague, setCurrentLeague] = useState(DEFAULT_LEAGUE);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const { leagues } = useLeagues();

  const handleSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const response = await fetch(`${API_URL}/recommendations/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          preferred_content: formData.preferredContent,
          profit_goal: formData.profitGoal,
          investment: formData.investment,
          league: currentLeague,
        }),
      });

      if (!response.ok) {
        throw new Error("추천 요청에 실패했습니다");
      }

      const data = await response.json();
      setRecommendations(data.results || []);
    } catch (err) {
      setError(err.message);
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <Header
        currentLeague={currentLeague}
        onLeagueChange={setCurrentLeague}
        leagues={leagues}
      />

      <main className="main-content">
        <div className="page-layout">
          {/* Left: Form */}
          <aside className="form-sidebar">
            <div className="sidebar-header">
              <h2>파밍 조건</h2>
              <p className="text-muted">원하는 콘텐츠와 수익 목표를 선택하세요</p>
            </div>
            <FarmingForm onSubmit={handleSubmit} loading={loading} />
          </aside>

          {/* Right: Results */}
          <section className="results-area">
            <div className="results-header">
              <h2>추천 파밍 루트</h2>
              {hasSearched && !loading && (
                <span className="results-count">
                  {recommendations.length}개 추천
                </span>
              )}
            </div>

            {!hasSearched && (
              <div className="empty-state">
                <div className="empty-icon">🗺️</div>
                <h3>파밍 루트를 추천받아 보세요</h3>
                <p>왼쪽에서 캐릭터 정보와 선호 콘텐츠를 설정한 후<br/>추천받기 버튼을 클릭하세요</p>
              </div>
            )}

            {loading && (
              <div className="loading-container">
                <div className="spinner"></div>
                <p>최적의 파밍 루트를 찾고 있습니다...</p>
              </div>
            )}

            {error && (
              <div className="error-message">
                <p>❌ {error}</p>
                <button onClick={() => setError(null)}>다시 시도</button>
              </div>
            )}

            {hasSearched && !loading && !error && recommendations.length === 0 && (
              <div className="empty-state">
                <div className="empty-icon">🔍</div>
                <h3>조건에 맞는 추천이 없습니다</h3>
                <p>다른 조건으로 다시 검색해 보세요</p>
              </div>
            )}

            {!loading && !error && recommendations.length > 0 && (
              <div className="recommendations-grid">
                {recommendations.map((rec, index) => (
                  <RecommendationCard
                    key={index}
                    recommendation={rec}
                    rank={index + 1}
                  />
                ))}
              </div>
            )}
          </section>
        </div>
      </main>

      <footer className="footer">
        <p>
          데이터 출처:{" "}
          <a href="https://poe2scout.com" target="_blank" rel="noopener noreferrer">
            poe2scout.com
          </a>
          {" · "}
          <a href="https://poe2db.tw/kr/" target="_blank" rel="noopener noreferrer">
            poe2db.tw
          </a>
        </p>
      </footer>
    </div>
  );
}
