import json
import os
from scrap.jobs.statistic import find_element_value, get_attribute_value

def debug_price_extraction():
    """
    Debug pour comprendre pourquoi seulement 14 annonces sur 70 ont un prix
    """
    data_dir = os.path.join("scrap", "tools", "scrap", "data")
    total_ads = 0
    ads_with_price = 0
    ads_without_price = 0
    price_errors = []
    
    print("🔍 Analyse des prix dans les annonces...")
    
    for file in os.listdir(data_dir):
        if file.startswith("ads_") and file.endswith(".json"):
            file_path = os.path.join(data_dir, file)
            print(f"\n📁 Fichier: {file}")
            
            try:
                with open(file_path, encoding="utf-8") as f:
                    data = json.load(f)
                
                if isinstance(data, list):
                    ads = data
                elif isinstance(data, dict):
                    ads = [data]
                else:
                    continue
                
                for i, ad in enumerate(ads):
                    total_ads += 1
                    
                    # Vérifie si l'annonce a un prix
                    price_values = find_element_value(ad, "price")
                    
                    if price_values:
                        print(f"  ✅ Annonce {i+1}: Prix trouvé = {price_values}")
                        ads_with_price += 1
                    else:
                        print(f"  ❌ Annonce {i+1}: Pas de prix trouvé")
                        ads_without_price += 1
                        
                        # Analyse pourquoi pas de prix
                        if "price" in ad:
                            print(f"     💡 'price' existe mais vide: {ad['price']}")
                        else:
                            print(f"     💡 Pas de clé 'price' dans l'annonce")
                        
                        # Liste les clés disponibles
                        keys = list(ad.keys())
                        print(f"     📋 Clés disponibles: {keys[:10]}...")  # Affiche les 10 premières
                        
                        price_errors.append({
                            "file": file,
                            "ad_index": i,
                            "ad_keys": keys,
                            "price_field": ad.get("price", "ABSENT")
                        })
                
            except Exception as e:
                print(f"❌ Erreur lecture {file}: {e}")
                continue
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"   Total annonces: {total_ads}")
    print(f"   Annonces avec prix: {ads_with_price}")
    print(f"   Annonces sans prix: {ads_without_price}")
    print(f"   Taux de réussite: {(ads_with_price/total_ads)*100:.1f}%")
    
    if price_errors:
        print(f"\n🔍 DÉTAILS des annonces sans prix:")
        for error in price_errors[:5]:  # Affiche les 5 premières erreurs
            print(f"   📄 {error['file']} - Annonce {error['ad_index']+1}")
            print(f"      Prix trouvé: {error['price_field']}")
            print(f"      Clés: {error['ad_keys'][:10]}...")

if __name__ == "__main__":
    debug_price_extraction() 