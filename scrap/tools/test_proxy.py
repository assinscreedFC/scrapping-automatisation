from curl_cffi import requests
from typing import List

def tester_proxies(proxies: List[str], url: str = "https://httpbin.org/ip") -> List[str]:
    proxies_valides = []

    for proxy in proxies:
        try:
            response = requests.get(
                url,
                proxies={"http": proxy, "https": proxy},
                timeout=10,
                impersonate="chrome110"  # Pour simuler un vrai navigateur
            )

            if response.status_code == 200:
                ip = response.json().get("origin", "Inconnue")
                print(f"✅ Proxy valide : {proxy} → IP : {ip}")
                proxies_valides.append(proxy)
            else:
                print(f"❌ Proxy invalide (status {response.status_code}) : {proxy}")

        except Exception as e:
            print(f"❌ Erreur avec le proxy {proxy} : {e}")

    return proxies_valides

import json

def charger_proxies_json_avance(chemin_fichier: str) -> list[dict]:
    """
    Charge les proxies depuis un fichier JSON contenant une liste de dictionnaires avec les clés 'http' et 'https'.
    Exemple de contenu :
    [
      {"http": "84.103.174.6:80", "https": "84.103.174.6:80"},
      ...
    ]
    """
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as fichier:
            proxies = json.load(fichier)
            return  proxies

    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")
        return []

def generater_proxy_json():
    pro = tester_proxies(charger_proxies_json_avance("scrap/config/proxies.json"))
    with open("scrap/config/proxies_validated.json", "w", encoding="utf-8") as fichier:
        json.dump(pro, fichier, indent=4)

if __name__ == "__main__":
    pro=tester_proxies(charger_proxies_json_avance("scrap/config/proxies.json"))
    with open("scrap/config/proxies_validated.json", "w", encoding="utf-8") as fichier:
        json.dump(pro, fichier, indent=4)