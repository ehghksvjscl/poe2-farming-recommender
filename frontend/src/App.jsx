import { useState, useEffect } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export default function App() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    level: 85,
    build_type: "콜드 DOT",
    preferred_content: "맵핑",
  });

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/recommendations/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      setRecommendations(data.results || []);
    } catch (error) {
      console.error("Failed to fetch recommendations:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div style={{ fontFamily: "sans-serif", padding: "32px" }}>
      <header>
        <h1>PoE2 Farming Recommender</h1>
        <p>조건에 맞는 파밍 루트를 추천합니다.</p>
      </header>

      <section style={{ marginTop: "24px" }}>
        <h2>추천 요청</h2>
        <div style={{ display: "grid", gap: "12px", maxWidth: "420px" }}>
          <label>
            캐릭터 레벨
            <input
              name="level"
              type="number"
              min="1"
              value={formData.level}
              onChange={handleChange}
              placeholder="예: 85"
              style={{ width: "100%" }}
            />
          </label>
          <label>
            빌드 유형
            <input
              name="build_type"
              type="text"
              value={formData.build_type}
              onChange={handleChange}
              placeholder="예: 콜드 DOT"
              style={{ width: "100%" }}
            />
          </label>
          <label>
            선호 콘텐츠
            <input
              name="preferred_content"
              type="text"
              value={formData.preferred_content}
              onChange={handleChange}
              placeholder="예: 맵핑"
              style={{ width: "100%" }}
            />
          </label>
          <button type="button" onClick={fetchRecommendations} disabled={loading}>
            {loading ? "로딩 중..." : "추천 받기"}
          </button>
        </div>
      </section>

      <section style={{ marginTop: "32px" }}>
        <h2>추천 결과</h2>
        <div style={{ display: "grid", gap: "16px" }}>
          {recommendations.length > 0 ? (
            recommendations.map((item, index) => (
              <article
                key={index}
                style={{
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                  padding: "16px",
                }}
              >
                <h3>{item.zone}</h3>
                <p>리그/시즌: {item.league}</p>
                <p>시간당 수익: {item.avg_profit_per_hour}</p>
                <p>보상 유형: {item.drop_focus}</p>
                <p>적합 빌드: {item.allowed_builds ? item.allowed_builds.join(", ") : ""}</p>
              </article>
            ))
          ) : (
            <p>추천 결과가 없습니다.</p>
          )}
        </div>
      </section>
    </div>
  );
}
