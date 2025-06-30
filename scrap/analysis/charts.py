from typing import List, Dict, Any, Optional
from .statistics import get_price_distribution, get_brand_statistics, get_location_statistics
from .filters import load_ads_data
import matplotlib.pyplot as plt
import io

def create_price_histogram(ads: List[Dict[str, Any]], max_bars: int = 10) -> str:
    """
    Crée un histogramme des prix en format texte pour Telegram
    """
    distribution = get_price_distribution(ads, max_bars)
    
    if not distribution["ranges"]:
        return "❌ Aucune donnée de prix disponible"
    
    chart = "📊 <b>Distribution des prix</b>\n\n"
    
    max_count = max(distribution["counts"]) if distribution["counts"] else 0
    
    for i, (range_name, count) in enumerate(zip(distribution["ranges"], distribution["counts"])):
        if max_count > 0:
            bar_length = int((count / max_count) * 20)  # 20 caractères max
            bar = "█" * bar_length
        else:
            bar = ""
        
        chart += f"{range_name}: {bar} ({count})\n"
    
    chart += f"\n📈 Total: {distribution['total_ads']} annonces"
    return chart

def create_brand_chart(ads: List[Dict[str, Any]], top_n: int = 10) -> str:
    """
    Crée un graphique des marques les plus populaires
    """
    brand_stats = get_brand_statistics(ads)
    
    if not brand_stats:
        return "❌ Aucune donnée de marque disponible"
    
    chart = f"🏷 <b>Top {top_n} des marques</b>\n\n"
    
    max_count = max(brand_stats.values()) if brand_stats else 0
    
    for i, (brand, count) in enumerate(list(brand_stats.items())[:top_n]):
        if max_count > 0:
            bar_length = int((count / max_count) * 15)  # 15 caractères max
            bar = "█" * bar_length
        else:
            bar = ""
        
        chart += f"{brand}: {bar} ({count})\n"
    
    return chart

def create_location_chart(ads: List[Dict[str, Any]], top_n: int = 10) -> str:
    """
    Crée un graphique des localisations les plus populaires
    """
    location_stats = get_location_statistics(ads)
    
    if not location_stats:
        return "❌ Aucune donnée de localisation disponible"
    
    chart = f"📍 <b>Top {top_n} des localisations</b>\n\n"
    
    max_count = max(location_stats.values()) if location_stats else 0
    
    for i, (location, count) in enumerate(list(location_stats.items())[:top_n]):
        if max_count > 0:
            bar_length = int((count / max_count) * 15)  # 15 caractères max
            bar = "█" * bar_length
        else:
            bar = ""
        
        chart += f"{location}: {bar} ({count})\n"
    
    return chart

def create_summary_chart() -> str:
    """
    Crée un résumé visuel complet des données
    """
    ads = load_ads_data()
    
    if not ads:
        return "❌ Aucune donnée disponible. Lancez d'abord /search"
    
    summary = f"📊 <b>Résumé des données</b>\n\n"
    summary += f"📦 Total annonces: {len(ads)}\n\n"
    
    # Ajoute l'histogramme des prix
    summary += create_price_histogram(ads) + "\n\n"
    
    # Ajoute le top des marques
    summary += create_brand_chart(ads, 5) + "\n\n"
    
    # Ajoute le top des localisations
    summary += create_location_chart(ads, 5)
    
    return summary

def get_valid_prices(ads: List[Dict[str, Any]]) -> List[float]:
    """
    Extrait tous les prix valides (float) des annonces
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
    from scrap.jobs.statistic import find_element_value
    for ad in ads:
        price_values = find_element_value(ad, "price")
        if price_values:
            for price_val in price_values if isinstance(price_values, list) else [price_values]:
                price_num = extract_first_number(price_val)
                if price_num is not None:
                    prices.append(price_num)
    return prices

def plot_price_histogram(ads: List[Dict[str, Any]], bins: int = 10) -> Optional[io.BytesIO]:
    """
    Génère un histogramme des prix et retourne un buffer BytesIO (image PNG)
    """
    prices = get_valid_prices(ads)
    if not prices:
        return None
    plt.figure(figsize=(8, 4))
    plt.hist(prices, bins=bins, color='skyblue', edgecolor='black')
    plt.title("Distribution des prix")
    plt.xlabel("Prix (€)")
    plt.ylabel("Nombre d'annonces")
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def plot_location_histogram(ads: List[Dict[str, Any]], top_n: int = 10) -> Optional[io.BytesIO]:
    """
    Génère un histogramme des villes et retourne un buffer BytesIO (image PNG)
    Utilise spécifiquement l'élément 'city'
    """
    from scrap.jobs.statistic import find_element_value
    
    city_counts = {}
    
    for ad in ads:
        # Utilise spécifiquement l'élément 'city'
        cities = find_element_value(ad, "city")
        if cities:
            city = str(cities[0] if isinstance(cities, list) else cities).strip()
            if city:
                city_counts[city] = city_counts.get(city, 0) + 1
    
    if not city_counts:
        return None
    
    # Trie par nombre d'occurrences décroissant
    sorted_cities = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Prend les top_n villes
    top_locations = sorted_cities[:top_n]
    locations = [loc[0] for loc in top_locations]
    counts = [loc[1] for loc in top_locations]
    
    # Augmente la taille de la figure pour accommoder les noms de villes
    plt.figure(figsize=(12, 7))
    bars = plt.bar(range(len(locations)), counts, color='lightgreen', edgecolor='black')
    plt.title(f"Top {top_n} des villes (élément 'city')")
    plt.xlabel("Villes")
    plt.ylabel("Nombre d'annonces")
    plt.xticks(range(len(locations)), locations, rotation=45, ha='right')
    
    # Ajoute les valeurs sur les barres
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(count), ha='center', va='bottom')
    
    # Ajuste les marges manuellement pour éviter le warning
    plt.subplots_adjust(bottom=0.2, left=0.1, right=0.95, top=0.9)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf 