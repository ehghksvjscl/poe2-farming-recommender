import { useState, useEffect } from "react";
import "./MarketItemList.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8001/api";

// 화폐 아이콘 URL
const CURRENCY_ICONS = {
  exalted: "https://web.poecdn.com//gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvQ3VycmVuY3lBZGRNb2RUb1JhcmUiLCJzY2FsZSI6MSwicmVhbG0iOiJwb2UyIn1d/ad7c366789/CurrencyAddModToRare.png",
  divine: "https://web.poecdn.com//gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvQ3VycmVuY3lNb2RWYWx1ZXMiLCJzY2FsZSI6MSwicmVhbG0iOiJwb2UyIn1d/2986e220b3/CurrencyModValues.png",
};

const CATEGORY_LABELS = {
  currency: "화폐",
  runes: "룬",
  essences: "에센스",
  fragments: "조각",
  waystones: "경로석",
  omens: "전조",
  breachstones: "균열석",
  deliriuminstill: "환영",
  uniques: "유니크",
  accessory: "장신구",
  armour: "방어구",
  weapon: "무기",
  jewel: "주얼",
  other: "기타",
};

function formatPrice(price) {
  if (!price && price !== 0) return "-";
  const num = parseFloat(price);
  
  if (num >= 10000) {
    return (num / 1000).toFixed(1) + "k";
  }
  if (num >= 1000) {
    return num.toLocaleString("ko-KR", { maximumFractionDigits: 0 });
  }
  if (num >= 100) {
    return num.toFixed(0);
  }
  if (num >= 1) {
    return num.toFixed(1);
  }
  return num.toFixed(2);
}

export default function MarketItemList() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [minPrice, setMinPrice] = useState(1);
  const [priceUnit, setPriceUnit] = useState("exalted"); // "exalted" or "divine"
  const [totalCount, setTotalCount] = useState(0);
  const [exchangeRates, setExchangeRates] = useState(null);

  useEffect(() => {
    fetchItems();
  }, [selectedCategory, minPrice, priceUnit]);

  const fetchItems = async () => {
    setLoading(true);
    setError(null);

    try {
      let url = `${API_URL}/market-items/?min_price=${minPrice}&unit=${priceUnit}`;
      if (selectedCategory) {
        url += `&category=${selectedCategory}`;
      }
      if (searchTerm) {
        url += `&search=${encodeURIComponent(searchTerm)}`;
      }

      const response = await fetch(url);
      if (!response.ok) {
        throw new Error("데이터를 불러오지 못했습니다");
      }

      const data = await response.json();
      setItems(data.items || []);
      setCategories(data.categories || []);
      setTotalCount(data.count || 0);
      setExchangeRates(data.exchange_rates || null);
    } catch (err) {
      setError(err.message);
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchItems();
  };

  return (
    <div className="market-list">
      {/* 필터 영역 */}
      <div className="market-filters">
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            placeholder="아이템 검색 (한글/영문)"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          <button type="submit" className="search-btn">
            검색
          </button>
        </form>

        <div className="filter-row">
          <label className="filter-label">
            단위:
            <select
              value={priceUnit}
              onChange={(e) => setPriceUnit(e.target.value)}
              className="filter-select unit-select"
            >
              <option value="exalted">Exalted Orb</option>
              <option value="divine">Divine Orb</option>
            </select>
          </label>

          <label className="filter-label">
            최소 가격:
            <select
              value={minPrice}
              onChange={(e) => setMinPrice(Number(e.target.value))}
              className="filter-select"
            >
              <option value={1}>1 {priceUnit === "divine" ? "div" : "ex"} 이상</option>
              <option value={5}>5 {priceUnit === "divine" ? "div" : "ex"} 이상</option>
              <option value={10}>10 {priceUnit === "divine" ? "div" : "ex"} 이상</option>
              <option value={50}>50 {priceUnit === "divine" ? "div" : "ex"} 이상</option>
              <option value={100}>100 {priceUnit === "divine" ? "div" : "ex"} 이상</option>
              <option value={500}>500 {priceUnit === "divine" ? "div" : "ex"} 이상</option>
            </select>
          </label>

          <label className="filter-label">
            카테고리:
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="filter-select"
            >
              <option value="">전체</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {CATEGORY_LABELS[cat] || cat}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="results-info">
          총 <strong>{totalCount.toLocaleString()}</strong>개 아이템
          {exchangeRates && (
            <span className="exchange-info">
              <img src={CURRENCY_ICONS.divine} alt="Divine" className="exchange-icon" />
              <span>1</span>
              <span className="exchange-equals">=</span>
              <img src={CURRENCY_ICONS.exalted} alt="Exalted" className="exchange-icon" />
              <span>{exchangeRates.exalted_per_divine}</span>
            </span>
          )}
        </div>
      </div>

      {/* 에러 */}
      {error && (
        <div className="market-error">
          <p>❌ {error}</p>
          <button onClick={fetchItems}>다시 시도</button>
        </div>
      )}

      {/* 로딩 */}
      {loading && (
        <div className="market-loading">
          <div className="spinner"></div>
          <p>아이템을 불러오는 중...</p>
        </div>
      )}

      {/* 아이템 리스트 */}
      {!loading && !error && (
        <div className="market-table-container">
          <table className="market-table">
            <thead>
              <tr>
                <th className="col-rank">#</th>
                <th className="col-icon"></th>
                <th className="col-name">아이템</th>
                <th className="col-category">카테고리</th>
                <th className="col-price">가격</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item, index) => (
                <tr key={item.id} className="item-row">
                  <td className="col-rank">{index + 1}</td>
                  <td className="col-icon">
                    {item.icon_url && (
                      <img
                        src={item.icon_url}
                        alt={item.name}
                        className="item-icon"
                        loading="lazy"
                      />
                    )}
                  </td>
                  <td className="col-name">
                    <div className="item-name">{item.name_ko || item.name}</div>
                    {item.name_ko && (
                      <div className="item-name-en">{item.name}</div>
                    )}
                  </td>
                  <td className="col-category">
                    <span className={`category-badge cat-${item.category}`}>
                      {CATEGORY_LABELS[item.category] || item.category}
                    </span>
                  </td>
                  <td className="col-price">
                    <div className="price-stack">
                      <div className="price-row price-ex">
                        <img src={CURRENCY_ICONS.exalted} alt="Exalted" className="currency-icon" />
                        <span className="price-value">{formatPrice(item.price_in_exalted)}</span>
                      </div>
                      <div className="price-row price-div">
                        <img src={CURRENCY_ICONS.divine} alt="Divine" className="currency-icon" />
                        <span className="price-value">{formatPrice(item.price_in_divine)}</span>
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {items.length === 0 && (
            <div className="no-items">
              <p>조건에 맞는 아이템이 없습니다</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

