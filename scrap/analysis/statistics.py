import statistics
from typing import List, Dict, Any, Optional, Tuple
from scrap.jobs.statistic import get_attribute_value, find_element_value
from .filters import load_ads_data

def get_price_statistics(ads: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Calcule les statistiques de prix pour une liste d'annonces
    """
    prices = []
    
    def extract_first_number(value):
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, list):
            if value:
                return extract_first_number(value[0])
        elif isinstance(value, str):
            try:
                return float(value.replace(" ", "").replace(",", "."))
            except (ValueError, TypeError):
                pass
        return None
    
    for ad in ads:
        # Utilise la fonction existante pour extraire le prix (élément)
        price_values = find_element_value(ad, "price")
        if price_values:
            for price_val in price_values if isinstance(price_values, list) else [price_values]:
                price_num = extract_first_number(price_val)
                if price_num is not None:
                    prices.append(price_num)
    
    if not prices:
        return {
            "count": 0,
            "min": 0,
            "max": 0,
            "mean": 0,
            "median": 0
        }
    
    return {
        "count": len(prices),
        "min": min(prices),
        "max": max(prices),
        "mean": statistics.mean(prices),
        "median": statistics.median(prices)
    }

def get_price_distribution(ads: List[Dict[str, Any]], bins: int = 10) -> Dict[str, Any]:
    """
    Calcule la distribution des prix par fourchettes
    """
    prices = []
    
    def extract_first_number(value):
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, list):
            if value:
                return extract_first_number(value[0])
        elif isinstance(value, str):
            try:
                return float(value.replace(" ", "").replace(",", "."))
            except (ValueError, TypeError):
                pass
        return None
    
    for ad in ads:
        # Utilise la fonction existante pour extraire le prix (élément)
        price_values = find_element_value(ad, "price")
        if price_values:
            for price_val in price_values if isinstance(price_values, list) else [price_values]:
                price_num = extract_first_number(price_val)
                if price_num is not None:
                    prices.append(price_num)
    
    if not prices:
        return {"ranges": [], "counts": []}
    
    min_price = min(prices)
    max_price = max(prices)
    bin_size = (max_price - min_price) / bins
    
    ranges = []
    counts = []
    
    for i in range(bins):
        start = min_price + i * bin_size
        end = min_price + (i + 1) * bin_size
        count = sum(1 for price in prices if start <= price < end)
        
        ranges.append(f"{start:.0f}-{end:.0f}€")
        counts.append(count)
    
    return {
        "ranges": ranges,
        "counts": counts,
        "total_ads": len(prices)
    }

def get_brand_statistics(ads: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Compte le nombre d'annonces par marque
    """
    brand_counts = {}
    
    for ad in ads:
        # Utilise la fonction existante pour extraire la marque
        brands = get_attribute_value(ad, "brand")
        if brands:
            brand = str(brands[0] if isinstance(brands, list) else brands).strip()
            if brand:
                brand_counts[brand] = brand_counts.get(brand, 0) + 1
    
    return dict(sorted(brand_counts.items(), key=lambda x: x[1], reverse=True))

def get_location_statistics(ads: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Compte le nombre d'annonces par localisation
    """
    location_counts = {}
    
    for ad in ads:
        # Essaie d'abord les attributs de localisation
        location = None
        for location_key in ["location", "city", "ville"]:
            locations = get_attribute_value(ad, location_key)
            if locations:
                location = str(locations[0] if isinstance(locations, list) else locations).strip()
                break
        
        # Si pas trouvé dans les attributs, essaie les éléments
        if not location:
            for location_key in ["location", "city", "ville"]:
                locations = find_element_value(ad, location_key)
                if locations:
                    location = str(locations[0] if isinstance(locations, list) else locations).strip()
                    break
        
        if location:
            location_counts[location] = location_counts.get(location, 0) + 1
    
    return dict(sorted(location_counts.items(), key=lambda x: x[1], reverse=True))

def get_summary_statistics() -> Dict[str, Any]:
    """
    Génère un résumé complet des statistiques
    """
    ads = load_ads_data()
    
    if not ads:
        return {
            "total_ads": 0,
            "price_stats": {},
            "brand_stats": {},
            "location_stats": {}
        }
    
    return {
        "total_ads": len(ads),
        "price_stats": get_price_statistics(ads),
        "price_distribution": get_price_distribution(ads),
        "brand_stats": get_brand_statistics(ads),
        "location_stats": get_location_statistics(ads)
    } 