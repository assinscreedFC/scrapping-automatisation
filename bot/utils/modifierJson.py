import json
import os


class FichierNonTrouveError(Exception):
    pass


class CleNonTrouveeError(Exception):
    pass


def modifier_fichier_json(chemin_fichier, cle, nouvelle_valeur):
    # Vérifie si le fichier existe
    if not os.path.exists(chemin_fichier):
        raise FichierNonTrouveError(f"Le fichier {chemin_fichier} n'a pas été trouvé.")

    # Charge le contenu JSON
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Vérifie si la clé existe
    if cle not in data:
        raise CleNonTrouveeError(f"La clé '{cle}' n'existe pas dans le fichier JSON.")

    # Modifie la valeur
    data[cle] = nouvelle_valeur

    # Sauvegarde les modifications
    with open(chemin_fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
