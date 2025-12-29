import PriceChart from "./PriceChart";
import { formatPrice, formatQuantity, formatDate } from "../utils/format";

export default function ItemDetail({ item, onClose }) {
  if (!item) return null;

  const validLogs = (item.priceLogs || []).filter(log => log !== null);

  return (
    <div className="item-detail-overlay" onClick={onClose}>
      <div className="item-detail" onClick={(e) => e.stopPropagation()}>
        <button className="item-detail__close" onClick={onClose}>✕</button>
        
        <div className="item-detail__header">
          <img 
            src={item.iconUrl} 
            alt={item.name || item.text}
            className="item-detail__icon"
          />
          <div className="item-detail__title">
            <h2>{item.name_ko || item.name || item.text}</h2>
            {item.name_ko && (item.name || item.text) !== item.name_ko && (
              <span className="item-detail__name-en">{item.name || item.text}</span>
            )}
            <span className="item-detail__category">
              {item.category_ko || item.categoryApiId}
            </span>
          </div>
        </div>

        <div className="item-detail__price-section">
          <div className="item-detail__current-price">
            <span className="item-detail__price-label">현재 가격</span>
            <span className="item-detail__price-value">
              {formatPrice(item.currentPrice)} <small>exalted</small>
            </span>
          </div>
        </div>

        <div className="item-detail__chart-section">
          <h3>가격 추이 (7일)</h3>
          <PriceChart item={item} height={180} />
        </div>

        <div className="item-detail__history">
          <h3>가격 기록</h3>
          <table className="item-detail__table">
            <thead>
              <tr>
                <th>시간</th>
                <th>가격</th>
                <th>매물 수</th>
              </tr>
            </thead>
            <tbody>
              {validLogs.map((log, i) => (
                <tr key={i}>
                  <td>{formatDate(log.time, true)}</td>
                  <td>{formatPrice(log.price)} ex</td>
                  <td>{formatQuantity(log.quantity)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

