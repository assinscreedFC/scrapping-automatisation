from scrap.infra.http_client import HttpClient

def test_homepage_leboncoin():
    client = HttpClient()
    url = "https://www.leboncoin.fr/ad/voitures/2933069016"
    html = client.get(url)
    if html:
        print("✅ Requête réussie.")
        print("🔎 Début du HTML :")
        print(html)
        #with open("resultat.txt", "w", encoding="utf-8") as f:
        #    f.write(html)
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
            return

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
            return

        tableau_ads_str = chaine[match_debut.start() + 6: i + 1]  # +6 pour passer '"ads":'

        # Parse le tableau en JSON
        ads_data = json.loads(tableau_ads_str)

        # Sauvegarde dans un fichier
        with open(fichier_sortie, "w", encoding="utf-8") as f:
            json.dump(ads_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Tableau 'ads' extrait et sauvegardé dans {fichier_sortie}")

    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON : {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")


if __name__ == "__main__":
    html=test_homepage_leboncoin()
    extraire_ads_et_sauvegarder(html)





