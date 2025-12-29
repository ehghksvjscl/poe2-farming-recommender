import "./CategoryTabs.css";

const CATEGORIES = [
  { id: "currency", label: "화폐", icon: "💰" },
  { id: "runes", label: "룬", icon: "🔮" },
  { id: "essences", label: "에센스", icon: "💎" },
  { id: "fragments", label: "조각", icon: "🔷" },
  { id: "omens", label: "전조", icon: "✨" },
  { id: "catalysts", label: "촉매", icon: "⚗️" },
  { id: "waystones", label: "경로석", icon: "🗺️" },
  { id: "lineagesupportgems", label: "혈통 젬", icon: "💠" },
];

export default function CategoryTabs({ activeCategory, onCategoryChange }) {
  return (
    <div className="category-tabs">
      <div className="category-tabs-inner">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.id}
            className={`category-tab ${activeCategory === cat.id ? "active" : ""}`}
            onClick={() => onCategoryChange(cat.id)}
          >
            <span className="category-icon">{cat.icon}</span>
            <span className="category-label">{cat.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

export { CATEGORIES };

