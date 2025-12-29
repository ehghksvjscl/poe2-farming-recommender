import { useState } from "react";
import "./FarmingForm.css";

const CONTENT_TYPES = [
  { id: "mapping", label: "맵핑", icon: "🗺️", desc: "경로석 파밍" },
  { id: "bossing", label: "보스", icon: "👹", desc: "보스 킬링" },
  { id: "expedition", label: "탐험", icon: "🧭", desc: "탐험 콘텐츠" },
  { id: "ritual", label: "의식", icon: "🕯️", desc: "의식 제단" },
  { id: "breach", label: "균열", icon: "💜", desc: "균열 파밍" },
  { id: "delirium", label: "환영", icon: "🌀", desc: "환영 콘텐츠" },
  { id: "heist", label: "강탈", icon: "🔓", desc: "강탈 계약서" },
  { id: "abyss", label: "심연", icon: "🕳️", desc: "심연 콘텐츠" },
];

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

export default function FarmingForm({ onSubmit, loading }) {
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
          {CONTENT_TYPES.map((content) => (
            <button
              key={content.id}
              type="button"
              className={`content-toggle ${
                formData.preferredContent.includes(content.id) ? "active" : ""
              }`}
              onClick={() => handleContentToggle(content.id)}
              title={content.desc}
            >
              <span className="content-icon">{content.icon}</span>
              <span className="content-label">{content.label}</span>
            </button>
          ))}
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

