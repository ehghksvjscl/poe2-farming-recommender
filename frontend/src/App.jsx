import { useState } from "react";
import "./index.css";
import Header from "./components/Header";
import FarmingGuide from "./components/FarmingGuide";
import MarketItemList from "./components/MarketItemList";
import { useLeagues } from "./hooks/useMarketData";

const DEFAULT_LEAGUE = "Fate of the Vaal";

export default function App() {
  const [currentLeague, setCurrentLeague] = useState(DEFAULT_LEAGUE);
  const [activeTab, setActiveTab] = useState("guide"); // "guide" | "market"

  const { leagues } = useLeagues();

  return (
    <div className="app">
      <Header
        currentLeague={currentLeague}
        onLeagueChange={setCurrentLeague}
        leagues={leagues}
      />

      <main className="main-content">
        {/* 탭 네비게이션 */}
        <nav className="tab-nav">
          <button
            className={`tab-btn ${activeTab === "guide" ? "active" : ""}`}
            onClick={() => setActiveTab("guide")}
          >
            📜 파밍 가이드
          </button>
          <button
            className={`tab-btn ${activeTab === "market" ? "active" : ""}`}
            onClick={() => setActiveTab("market")}
          >
            💰 시장 시세
          </button>
        </nav>

        {/* 파밍 가이드 탭 */}
        {activeTab === "guide" && (
          <div className="tab-content">
            <FarmingGuide />
          </div>
        )}

        {/* 마켓 시세 탭 */}
        {activeTab === "market" && (
          <div className="tab-content">
            <div className="tab-header">
              <h2>💰 1 Divine 이상 아이템 시세</h2>
              <p className="text-muted">poe2scout.com 기준 실시간 시세</p>
            </div>
            <MarketItemList />
          </div>
        )}
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
