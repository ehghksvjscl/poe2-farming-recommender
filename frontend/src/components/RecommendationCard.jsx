import "./RecommendationCard.css";

const DIFFICULTY_COLORS = {
  easy: "green",
  medium: "blue",
  hard: "gold",
  endgame: "red",
};

const DIFFICULTY_LABELS = {
  easy: "쉬움",
  medium: "보통",
  hard: "어려움",
  endgame: "엔드게임",
};

export default function RecommendationCard({ recommendation, rank }) {
  const {
    zone,
    league,
    avg_profit_per_hour,
    drop_focus,
    allowed_builds,
    reason,
    difficulty = "medium",
    exp_per_hour,
    requirements,
  } = recommendation;

  return (
    <article className="recommendation-card">
      <div className="card-header">
        <div className="card-rank">#{rank}</div>
        <div className="card-title-area">
          <h3 className="card-title">{zone}</h3>
          <span className="card-league">{league}</span>
        </div>
        <div className={`card-difficulty badge ${DIFFICULTY_COLORS[difficulty]}`}>
          {DIFFICULTY_LABELS[difficulty]}
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
        
        {exp_per_hour && (
          <div className="stat">
            <span className="stat-icon">⭐</span>
            <div className="stat-content">
              <span className="stat-value">{exp_per_hour}</span>
              <span className="stat-label">시간당 경험치</span>
            </div>
          </div>
        )}

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

      {allowed_builds && allowed_builds.length > 0 && (
        <div className="card-builds">
          <span className="builds-label">적합 빌드:</span>
          <div className="builds-tags">
            {allowed_builds.map((build) => (
              <span key={build} className="build-tag">{build}</span>
            ))}
          </div>
        </div>
      )}

      {requirements && (
        <div className="card-requirements">
          <h4>준비물</h4>
          <p>{requirements}</p>
        </div>
      )}

      <div className="card-actions">
        <button className="secondary">상세 보기</button>
        <button className="secondary">북마크</button>
      </div>
    </article>
  );
}

