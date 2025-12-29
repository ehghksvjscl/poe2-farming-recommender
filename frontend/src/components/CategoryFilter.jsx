const CATEGORIES = [
  { id: "all", label: "전체", icon: "📦" },
  { id: "currency", label: "화폐", icon: "💰" },
  { id: "runes", label: "룬", icon: "🔮" },
  { id: "essences", label: "에센스", icon: "✨" },
  { id: "fragments", label: "조각", icon: "💎" },
  { id: "omens", label: "전조", icon: "🌙" },
  { id: "catalysts", label: "촉매", icon: "⚗️" },
  { id: "waystones", label: "경로석", icon: "🗺️" },
  { id: "ritual", label: "의식", icon: "🎭" },
  { id: "delirium", label: "환영", icon: "👁️" },
  { id: "breach", label: "균열", icon: "🌀" },
  { id: "ultimatum", label: "얼티메이텀", icon: "⚔️" },
];

export default function CategoryFilter({ selected, onChange }) {
  return (
    <div className="category-filter">
      {CATEGORIES.map((cat) => (
        <button
          key={cat.id}
          className={`category-filter__btn ${selected === cat.id ? "active" : ""}`}
          onClick={() => onChange(cat.id)}
        >
          <span className="category-filter__icon">{cat.icon}</span>
          <span className="category-filter__label">{cat.label}</span>
        </button>
      ))}
    </div>
  );
}

export { CATEGORIES };

