import json
import os
import re
from typing import List, Dict, Any, Optional
from scrap.jobs.statistic import get_attribute_value, find_element_value

def load_ads_data() -> List[Dict[str, Any]]:
    """
    Charge toutes les données d'annonces depuis les fichiers ads_*.json
    """
    data_dir = os.path.join("scrap", "tools", "scrap", "data")
    all_ads = []
    
    if not os.path.exists(data_dir):
        return all_ads
        
    for file in os.listdir(data_dir):
        if file.startswith("ads_") and file.endswith(".json"):
            file_path = os.path.join(data_dir, file)
            try:
                with open(file_path, encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_ads.extend(data)
                    elif isinstance(data, dict):
                        all_ads.append(data)
            except Exception as e:
                print(f"Erreur lecture {file}: {e}")
                continue
    
    return all_ads

def extract_price(ad: Dict[str, Any]) -> Optional[float]:
    """
    Extrait le prix d'une annonce en utilisant les fonctions existantes
    """
    # Utilise la fonction existante find_element_value car price est un élément
    prices = find_element_value(ad, "price")
    if not prices:
        return None
    
    # Gère les listes imbriquées et extrait la première valeur numérique
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
    
    # Essaie d'extraire un prix de la première valeur trouvée
    first_price = prices[0] if isinstance(prices, list) else prices
    price_value = extract_first_number(first_price)
    
    return price_value

def extract_location(ad: Dict[str, Any]) -> Optional[str]:
    """
    Extrait la ville d'une annonce en utilisant uniquement l'élément 'city'.
    """
    cities = find_element_value(ad, "city")
    if cities:
        return str(cities[0]) if isinstance(cities, list) else str(cities)
    return None

def filter_by_price(ads: List[Dict[str, Any]], min_price: Optional[float] = None, max_price: Optional[float] = None) -> List[Dict[str, Any]]:
    """
    Filtre les annonces par fourchette de prix
    """
    filtered_ads = []
    
    for ad in ads:
        price = extract_price(ad)
        if price is None:
            continue
            
        if min_price is not None and price < min_price:
            continue
        if max_price is not None and price > max_price:
            continue
            
        filtered_ads.append(ad)
    
    return filtered_ads

def filter_by_location(ads: List[Dict[str, Any]], location_keywords: List[str]) -> List[Dict[str, Any]]:
    """
    Filtre les annonces par mots-clés de localisation
    """
    filtered_ads = []
    
    for ad in ads:
        location = extract_location(ad)
        if location is None:
            continue
            
        location_lower = location.lower()
        for keyword in location_keywords:
            if keyword.lower() in location_lower:
                filtered_ads.append(ad)
                break
    
    return filtered_ads

def filter_ads(ads: List[Dict[str, Any]], 
               min_price: Optional[float] = None, 
               max_price: Optional[float] = None,
               location_keywords: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Filtre les annonces avec tous les critères
    """
    filtered = ads
    
    # Filtre par prix
    if min_price is not None or max_price is not None:
        filtered = filter_by_price(filtered, min_price, max_price)
    
    # Filtre par localisation
    if location_keywords:
        filtered = filter_by_location(filtered, location_keywords)
    
    return filtered 