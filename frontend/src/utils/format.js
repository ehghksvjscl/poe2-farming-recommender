/**
 * Format price with appropriate decimal places
 */
export function formatPrice(price) {
  if (price === null || price === undefined) return "-";
  
  if (price >= 1000) {
    return `${(price / 1000).toFixed(1)}k`;
  }
  if (price >= 100) {
    return price.toFixed(0);
  }
  if (price >= 1) {
    return price.toFixed(1);
  }
  if (price >= 0.01) {
    return price.toFixed(2);
  }
  return price.toFixed(3);
}

/**
 * Format quantity with k/m suffixes
 */
export function formatQuantity(quantity) {
  if (quantity === null || quantity === undefined) return "-";
  
  if (quantity >= 1000000) {
    return `${(quantity / 1000000).toFixed(1)}M`;
  }
  if (quantity >= 1000) {
    return `${(quantity / 1000).toFixed(1)}K`;
  }
  return quantity.toLocaleString();
}

/**
 * Format date/time
 */
export function formatDate(dateString, includeTime = false) {
  if (!dateString) return "-";
  
  const date = new Date(dateString);
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  if (includeTime) {
    const hours = date.getHours().toString().padStart(2, "0");
    const minutes = date.getMinutes().toString().padStart(2, "0");
    return `${month}/${day} ${hours}:${minutes}`;
  }
  
  return `${month}/${day}`;
}

