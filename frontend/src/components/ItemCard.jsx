import "./ItemCard.css";

function formatPrice(price) {
  if (price === null || price === undefined || price === 0) return "-";
  if (price >= 1000) return `${(price / 1000).toFixed(1)}k`;
  if (price >= 1) return price.toFixed(1);
  return price.toFixed(2);
}

function getPriceChange(priceLogs) {
  if (!priceLogs || priceLogs.length < 2) return null;
  
  const validPrices = priceLogs.filter(p => p && p.price);
  if (validPrices.length < 2) return null;
  
  const current = validPrices[0].price;
  const previous = validPrices[validPrices.length - 1].price;
  
  if (previous === 0) return null;
  const change = ((current - previous) / previous) * 100;
  return change;
}

export default function ItemCard({ item }) {
  const { 
    name, 
    name_ko, 
    text,
    iconUrl, 
    currentPrice, 
    priceLogs,
    categoryApiId,
    category_ko,
    quantity
  } = item;

  const displayName = name_ko || name || text;
  const englishName = name || text;
  const priceChange = getPriceChange(priceLogs);
  const latestQuantity = priceLogs?.[0]?.quantity;

  return (
    <div className="item-card">
      <div className="item-card-icon">
        {iconUrl ? (
          <img 
            src={iconUrl} 
            alt={displayName} 
            loading="lazy"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        ) : (
          <div className="item-card-icon-placeholder">?</div>
        )}
      </div>
      
      <div className="item-card-info">
        <h3 className="item-card-name" title={englishName}>
          {displayName}
        </h3>
        {name_ko && englishName !== name_ko && (
          <span className="item-card-name-en">{englishName}</span>
        )}
        <div className="item-card-category">
          {category_ko || categoryApiId}
        </div>
      </div>

      <div className="item-card-price">
        <div className="price-current">
          <span className="price-value">{formatPrice(currentPrice)}</span>
          <span className="price-unit">exalted</span>
        </div>
        
        {priceChange !== null && (
          <div className={`price-change ${priceChange >= 0 ? 'up' : 'down'}`}>
            {priceChange >= 0 ? '▲' : '▼'} {Math.abs(priceChange).toFixed(1)}%
          </div>
        )}
        
        {latestQuantity && (
          <div className="item-quantity">
            수량: {latestQuantity.toLocaleString()}
          </div>
        )}
      </div>
    </div>
  );
}

