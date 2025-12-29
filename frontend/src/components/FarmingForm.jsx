import { useState } from "react";
import "./FarmingForm.css";

const BUILD_TYPES = [
  "콜드 DOT", "화염 DOT", "번개 빌드", "물리 빌드",
  "미니언", "토템", "트랩/마인", "활 빌드", "근접 빌드"
];

const CONTENT_TYPES = [
  { id: "mapping", label: "맵핑", icon: "🗺️" },
  { id: "bossing", label: "보스", icon: "👹" },
  { id: "delve", label: "델브", icon: "⛏️" },
  { id: "expedition", label: "탐험", icon: "🧭" },
  { id: "ritual", label: "의식", icon: "🕯️" },
  { id: "breach", label: "균열", icon: "💜" },
  { id: "delirium", label: "환영", icon: "🌀" },
];

const DIFFICULTY_LEVELS = [
  { value: "easy", label: "쉬움" },
  { value: "medium", label: "보통" },
  { value: "hard", label: "어려움" },
  { value: "endgame", label: "엔드게임" },
];

export default function FarmingForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    level: 85,
    buildType: "",
    preferredContent: [],
    difficulty: "medium",
    profitGoal: "",
    playTime: "",
    partySize: 1,
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
        <h3 className="form-section-title">캐릭터 정보</h3>
        
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="level">캐릭터 레벨</label>
            <input
              id="level"
              name="level"
              type="number"
              min="1"
              max="100"
              value={formData.level}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="buildType">빌드 유형</label>
            <select
              id="buildType"
              name="buildType"
              value={formData.buildType}
              onChange={handleChange}
            >
              <option value="">선택하세요</option>
              {BUILD_TYPES.map((build) => (
                <option key={build} value={build}>{build}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="partySize">파티 인원</label>
            <select
              id="partySize"
              name="partySize"
              value={formData.partySize}
              onChange={handleChange}
            >
              <option value={1}>솔로</option>
              <option value={2}>2인</option>
              <option value={3}>3인</option>
              <option value={4}>4인</option>
              <option value={5}>5인</option>
              <option value={6}>6인</option>
            </select>
          </div>
        </div>
      </div>

      <div className="form-section">
        <h3 className="form-section-title">선호 콘텐츠</h3>
        <div className="content-toggles">
          {CONTENT_TYPES.map((content) => (
            <button
              key={content.id}
              type="button"
              className={`content-toggle ${
                formData.preferredContent.includes(content.id) ? "active" : ""
              }`}
              onClick={() => handleContentToggle(content.id)}
            >
              <span className="content-icon">{content.icon}</span>
              <span className="content-label">{content.label}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="form-section">
        <h3 className="form-section-title">목표 설정</h3>
        
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="difficulty">선호 난이도</label>
            <select
              id="difficulty"
              name="difficulty"
              value={formData.difficulty}
              onChange={handleChange}
            >
              {DIFFICULTY_LEVELS.map((diff) => (
                <option key={diff.value} value={diff.value}>{diff.label}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="profitGoal">시간당 수익 목표 (Divine)</label>
            <input
              id="profitGoal"
              name="profitGoal"
              type="number"
              min="0"
              step="0.1"
              placeholder="예: 5"
              value={formData.profitGoal}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="playTime">플레이 가능 시간 (분)</label>
            <input
              id="playTime"
              name="playTime"
              type="number"
              min="0"
              placeholder="예: 60"
              value={formData.playTime}
              onChange={handleChange}
            />
          </div>
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

