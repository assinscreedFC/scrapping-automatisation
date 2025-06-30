from scrap.infra.http_client import HttpClient
from scrap.infra.proxy_pool import ProxyPool
def test_homepage_leboncoin():
    client = HttpClient()
    url = "https://www.leboncoin.fr/ad/voitures/2997258439"
    html = client.get(url)
    if html:
        print("✅ Requête réussie.")
        print("🔎 Début du HTML :")
        print(html)
        with open("resultat.txt", "w", encoding="utf-8") as f:
            f.write(html)
        #return html
    else:
        print("❌ Échec de la requête.")

import re
import json


def extraire_ads_et_sauvegarder(chaine: str, fichier_sortie: str = "ads.json"):
    try:
        # On cherche le début du tableau "ads":[
        match_debut = re.search(r'"ads"\s*:\s*\[', chaine)
        if not match_debut:
            print("❌ Clé 'ads' non trouvée.")
            return 0

        start = match_debut.end()  # Position juste après le '['
        bracket_count = 1
        i = start

        # Parcours caractère par caractère pour équilibrer les crochets
        while i < len(chaine):
            if chaine[i] == "[":
                bracket_count += 1
            elif chaine[i] == "]":
                bracket_count -= 1
                if bracket_count == 0:
                    break
            i += 1

        if bracket_count != 0:
            print("❌ Tableau 'ads' mal formé (crochets non équilibrés).")
            return 0

        tableau_ads_str = chaine[match_debut.start() + 6: i + 1]  # +6 pour passer '"ads":'

        # Parse le tableau en JSON
        ads_data = json.loads(tableau_ads_str)

        # Sauvegarde dans un fichier
        with open(fichier_sortie, "w", encoding="utf-8") as f:
            json.dump(ads_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Tableau 'ads' extrait et sauvegardé dans {fichier_sortie}")
        return len(ads_data)

    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON : {e}")
        return 0
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        return 0

def test():
    proxy_pool = ProxyPool()
    # proxy_pool.extract_proxy()
    client = HttpClient()
    for i in range(2):
        url = f"https://www.leboncoin.fr/recherche?text=clio+4&page={i + 1}"
        html = client.get(url,proxy=proxy_pool.get_first_proxy())
        extraire_ads_et_sauvegarder(html, f"ads_{i + 1}.json")
        proxy_pool.round_proxy()
if __name__ == "__main__":
    #html=test_homepage_leboncoin()
    #extraire_ads_et_sauvegarder(html)
    #teste scrapp avec pool proxy 3 page teste pour voir le resulta ads123
    test_homepage_leboncoin()





