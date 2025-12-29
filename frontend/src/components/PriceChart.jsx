import { useMemo } from "react";
import { formatPrice, formatDate } from "../utils/format";

export default function PriceChart({ item, height = 120 }) {
  const chartData = useMemo(() => {
    if (!item?.priceLogs) return [];
    
    return item.priceLogs
      .map((log, index) => ({
        index,
        price: log?.price ?? null,
        quantity: log?.quantity ?? null,
        time: log?.time ?? null,
      }))
      .filter(d => d.price !== null)
      .reverse();
  }, [item]);

  if (chartData.length === 0) {
    return (
      <div className="price-chart price-chart--empty">
        <span>가격 데이터 없음</span>
      </div>
    );
  }

  const prices = chartData.map(d => d.price);
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const range = maxPrice - minPrice || 1;

  const width = 300;
  const padding = { top: 10, right: 10, bottom: 30, left: 50 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;

  const points = chartData.map((d, i) => {
    const x = padding.left + (i / (chartData.length - 1 || 1)) * chartWidth;
    const y = padding.top + chartHeight - ((d.price - minPrice) / range) * chartHeight;
    return { x, y, ...d };
  });

  const linePath = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
  
  const areaPath = `
    ${linePath}
    L ${points[points.length - 1].x} ${padding.top + chartHeight}
    L ${points[0].x} ${padding.top + chartHeight}
    Z
  `;

  return (
    <div className="price-chart">
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
        <defs>
          <linearGradient id="priceGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="var(--color-accent)" stopOpacity="0.3" />
            <stop offset="100%" stopColor="var(--color-accent)" stopOpacity="0" />
          </linearGradient>
        </defs>
        
        {/* Grid lines */}
        {[0, 0.25, 0.5, 0.75, 1].map((ratio) => {
          const y = padding.top + chartHeight * (1 - ratio);
          const price = minPrice + range * ratio;
          return (
            <g key={ratio}>
              <line
                x1={padding.left}
                y1={y}
                x2={width - padding.right}
                y2={y}
                stroke="var(--color-border)"
                strokeDasharray="2,2"
                opacity="0.3"
              />
              <text
                x={padding.left - 5}
                y={y + 4}
                textAnchor="end"
                fontSize="10"
                fill="var(--color-text-secondary)"
              >
                {formatPrice(price)}
              </text>
            </g>
          );
        })}

        {/* Area fill */}
        <path d={areaPath} fill="url(#priceGradient)" />
        
        {/* Line */}
        <path
          d={linePath}
          fill="none"
          stroke="var(--color-accent)"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        
        {/* Data points */}
        {points.map((p, i) => (
          <g key={i}>
            <circle
              cx={p.x}
              cy={p.y}
              r="4"
              fill="var(--color-bg)"
              stroke="var(--color-accent)"
              strokeWidth="2"
            />
            {i === 0 || i === points.length - 1 ? (
              <text
                x={p.x}
                y={height - 10}
                textAnchor="middle"
                fontSize="9"
                fill="var(--color-text-secondary)"
              >
                {formatDate(p.time)}
              </text>
            ) : null}
          </g>
        ))}
      </svg>
    </div>
  );
}

