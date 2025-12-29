import "./RecommendationCard.css";

const INVESTMENT_COLORS = {
  zero: "green",
  low: "blue",
  medium: "gold",
  high: "red",
};

const INVESTMENT_LABELS = {
  zero: "무자본",
  low: "소자본",
  medium: "중자본",
  high: "대자본",
};

export default function RecommendationCard({ recommendation, rank }) {
  const {
    zone,
    league,
    avg_profit_per_hour,
    drop_focus,
    reason,
    investment = "low",
    requirements,
    strategy,
    tips,
  } = recommendation;

  return (
    <article className="recommendation-card">
      <div className="card-header">
        <div className="card-rank">#{rank}</div>
        <div className="card-title-area">
          <h3 className="card-title">{zone}</h3>
          <span className="card-league">{league}</span>
        </div>
        <div className={`card-investment badge ${INVESTMENT_COLORS[investment]}`}>
          {INVESTMENT_LABELS[investment]}
        </div>
      </div>

      <div className="card-stats">
        <div className="stat">
          <span className="stat-icon">💰</span>
          <div className="stat-content">
            <span className="stat-value">{avg_profit_per_hour}</span>
            <span className="stat-label">시간당 수익</span>
          </div>
        </div>

        <div className="stat">
          <span className="stat-icon">🎁</span>
          <div className="stat-content">
            <span className="stat-value">{drop_focus}</span>
            <span className="stat-label">주요 보상</span>
          </div>
        </div>
      </div>

      <div className="card-reason">
        <span className="reason-icon">💡</span>
        <p>{reason}</p>
      </div>

      {strategy && (
        <div className="card-strategy">
          <h4>🎮 파밍 전략</h4>
          <p>{strategy}</p>
        </div>
      )}

      {requirements && (
        <div className="card-requirements">
          <h4>📦 필요 준비물</h4>
          <p>{requirements}</p>
        </div>
      )}

      {tips && (
        <div className="card-tips">
          <h4>✨ 팁</h4>
          <p>{tips}</p>
        </div>
      )}

      <div className="card-actions">
        <button className="secondary">상세 가이드</button>
        <button className="secondary">북마크</button>
      </div>
    </article>
  );
}

