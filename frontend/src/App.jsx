const sampleRecommendations = [
  {
    zone: "Drowned City",
    league: "Standard",
    avgProfitPerHour: "3.2 Divine",
    dropFocus: "지도, 유니크",
    allowedBuilds: ["콜드 DOT", "활 빌드"],
  },
  {
    zone: "Crystal Vault",
    league: "Season 1",
    avgProfitPerHour: "4.1 Divine",
    dropFocus: "카드, 통화",
    allowedBuilds: ["토템", "미니언"],
  },
];

export default function App() {
  return (
    <div style={{ fontFamily: "sans-serif", padding: "32px" }}>
      <header>
        <h1>PoE2 Farming Recommender</h1>
        <p>조건에 맞는 파밍 루트를 추천합니다.</p>
      </header>

      <section style={{ marginTop: "24px" }}>
        <h2>추천 요청</h2>
        <form style={{ display: "grid", gap: "12px", maxWidth: "420px" }}>
          <label>
            캐릭터 레벨
            <input type="number" min="1" placeholder="예: 85" style={{ width: "100%" }} />
          </label>
          <label>
            빌드 유형
            <input type="text" placeholder="예: 콜드 DOT" style={{ width: "100%" }} />
          </label>
          <label>
            선호 콘텐츠
            <input type="text" placeholder="예: 맵핑" style={{ width: "100%" }} />
          </label>
          <button type="button">추천 받기</button>
        </form>
      </section>

      <section style={{ marginTop: "32px" }}>
        <h2>추천 결과</h2>
        <div style={{ display: "grid", gap: "16px" }}>
          {sampleRecommendations.map((item) => (
            <article
              key={item.zone}
              style={{
                border: "1px solid #ddd",
                borderRadius: "8px",
                padding: "16px",
              }}
            >
              <h3>{item.zone}</h3>
              <p>리그/시즌: {item.league}</p>
              <p>시간당 수익: {item.avgProfitPerHour}</p>
              <p>보상 유형: {item.dropFocus}</p>
              <p>적합 빌드: {item.allowedBuilds.join(", ")}</p>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
