import { useState, useEffect, useCallback } from "react";

const POE2SCOUT_API = "https://poe2scout.com/api";

export function useLeagues() {
  const [leagues, setLeagues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchLeagues() {
      try {
        const res = await fetch(`${POE2SCOUT_API}/leagues`);
        if (!res.ok) throw new Error("Failed to fetch leagues");
        const data = await res.json();
        setLeagues(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchLeagues();
  }, []);

  return { leagues, loading, error };
}

export function useMarketData(league, category) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchItems = useCallback(async () => {
    if (!league || !category) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const leagueEncoded = encodeURIComponent(league);
      const res = await fetch(
        `${POE2SCOUT_API}/items?category=${category}&league=${leagueEncoded}`
      );
      
      if (!res.ok) throw new Error("Failed to fetch items");
      
      const data = await res.json();
      setItems(data);
    } catch (err) {
      setError(err.message);
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [league, category]);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  return { items, loading, error, refetch: fetchItems };
}

export function filterAndSortItems(items, { searchQuery, sortBy }) {
  let filtered = [...items];

  // Search filter
  if (searchQuery) {
    const query = searchQuery.toLowerCase();
    filtered = filtered.filter(item => {
      const name = (item.name || item.text || "").toLowerCase();
      const nameKo = (item.name_ko || "").toLowerCase();
      return name.includes(query) || nameKo.includes(query);
    });
  }

  // Sort
  filtered.sort((a, b) => {
    const priceA = a.currentPrice || 0;
    const priceB = b.currentPrice || 0;
    const nameA = a.name_ko || a.name || a.text || "";
    const nameB = b.name_ko || b.name || b.text || "";
    
    const getChange = (item) => {
      if (!item.priceLogs || item.priceLogs.length < 2) return 0;
      const validPrices = item.priceLogs.filter(p => p && p.price);
      if (validPrices.length < 2) return 0;
      const current = validPrices[0].price;
      const previous = validPrices[validPrices.length - 1].price;
      return previous === 0 ? 0 : ((current - previous) / previous) * 100;
    };
    
    const quantityA = a.priceLogs?.[0]?.quantity || 0;
    const quantityB = b.priceLogs?.[0]?.quantity || 0;

    switch (sortBy) {
      case "price-desc":
        return priceB - priceA;
      case "price-asc":
        return priceA - priceB;
      case "name-asc":
        return nameA.localeCompare(nameB, "ko");
      case "change-desc":
        return getChange(b) - getChange(a);
      case "change-asc":
        return getChange(a) - getChange(b);
      case "quantity-desc":
        return quantityB - quantityA;
      default:
        return priceB - priceA;
    }
  });

  return filtered;
}

