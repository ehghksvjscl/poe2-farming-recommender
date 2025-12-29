import { useState } from "react";
import "./FarmingForm.css";

const PROFIT_GOALS = [
  { value: "low", label: "💵 낮음", desc: "1-3 Divine/시간" },
  { value: "medium", label: "💰 보통", desc: "3-7 Divine/시간" },
  { value: "high", label: "💎 높음", desc: "7-15 Divine/시간" },
  { value: "extreme", label: "🏆 최고", desc: "15+ Divine/시간" },
];

const INVESTMENT_LEVELS = [
  { value: "zero", label: "무자본", desc: "초기 투자 없음" },
  { value: "low", label: "소자본", desc: "1-10 Divine" },
  { value: "medium", label: "중자본", desc: "10-50 Divine" },
  { value: "high", label: "대자본", desc: "50+ Divine" },
];

export default function FarmingForm({
  onSubmit,
  loading,
  contentTypes = [],
  contentError = null,
}) {
  const [formData, setFormData] = useState({
    preferredContent: [],
    profitGoal: "medium",
    investment: "low",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleContentToggle = (contentId) => {
    setFormData((prev) => ({
      ...prev,
      preferredContent: prev.preferredContent.includes(contentId)
        ? prev.preferredContent.filter((id) => id !== contentId)
        : [...prev.preferredContent, contentId],
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form className="farming-form" onSubmit={handleSubmit}>
      <div className="form-section">
        <h3 className="form-section-title">선호 콘텐츠</h3>
        <p className="form-section-desc">파밍하고 싶은 콘텐츠를 선택하세요 (복수 선택 가능)</p>
        <div className="content-toggles">
          {contentTypes.map((content) => (
            <button
              key={content.key}
              type="button"
              className={`content-toggle ${
                formData.preferredContent.includes(content.key) ? "active" : ""
              }`}
              onClick={() => handleContentToggle(content.key)}
              title={content.description}
            >
              <span className="content-icon">
                <img src={content.icon_url} alt={content.label} loading="lazy" />
              </span>
              <span className="content-label">{content.label}</span>
            </button>
          ))}
          {contentError && (
            <div className="content-empty">콘텐츠 정보를 불러오지 못했습니다.</div>
          )}
          {!contentError && contentTypes.length === 0 && (
            <div className="content-empty">콘텐츠 정보를 불러오는 중...</div>
          )}
        </div>
      </div>

      <div className="form-section">
        <h3 className="form-section-title">수익 목표</h3>
        <div className="option-cards">
          {PROFIT_GOALS.map((goal) => (
            <label
              key={goal.value}
              className={`option-card ${formData.profitGoal === goal.value ? "active" : ""}`}
            >
              <input
                type="radio"
                name="profitGoal"
                value={goal.value}
                checked={formData.profitGoal === goal.value}
                onChange={handleChange}
              />
              <span className="option-label">{goal.label}</span>
              <span className="option-desc">{goal.desc}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="form-section">
        <h3 className="form-section-title">초기 투자 자본</h3>
        <div className="option-cards">
          {INVESTMENT_LEVELS.map((level) => (
            <label
              key={level.value}
              className={`option-card ${formData.investment === level.value ? "active" : ""}`}
            >
              <input
                type="radio"
                name="investment"
                value={level.value}
                checked={formData.investment === level.value}
                onChange={handleChange}
              />
              <span className="option-label">{level.label}</span>
              <span className="option-desc">{level.desc}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="form-actions">
        <button type="submit" disabled={loading}>
          {loading ? "추천 중..." : "🎯 파밍 루트 추천받기"}
        </button>
      </div>
    </form>
  );
}
