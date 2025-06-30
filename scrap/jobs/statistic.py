import json
import os
from pathlib import Path

# Exemple de données (pour test)
data = [
    {
        "owner": {"store_id": "14905556", "user_id": "abc"},
        "attributes": [
            {"key": "brand", "value": "Renault"},
            {"key": "model", "value": "Clio"}
        ]
    },
    {
        "owner": {"store_id": "22223333", "user_id": "def"},
        "attributes": [
            {"key": "brand", "value": "Peugeot"},
            {"key": "model", "value": "208"}
        ]
    }
]

def get_attribute_value(data, attribute_key, index=None):
    """
    Récupère les valeurs des attributs dont 'key' == attribute_key.
    Si index est None, renvoie la liste complète.
    Si un index est fourni, renvoie la valeur à cet index ou None.
    """
    results = []
    if isinstance(data, dict):
        if "attributes" in data and isinstance(data["attributes"], list):
            for attr in data["attributes"]:
                if attr.get("key") == attribute_key:
                    results.append(attr.get("value"))
        for v in data.values():
            sub = get_attribute_value(v, attribute_key)
            if isinstance(sub, list):
                results.extend(sub)
    elif isinstance(data, list):
        for item in data:
            sub = get_attribute_value(item, attribute_key)
            if isinstance(sub, list):
                results.extend(sub)
    if index is None:
        return results
    else:
        return results[index] if 0 <= index < len(results) else None

def find_element_value(data, element_name, index=None):
    """
    Récupère les valeurs de la clé element_name dans tout le JSON.
    Si index est None, renvoie la liste complète.
    Si un index est fourni, renvoie la valeur à cet index ou None.
    """
    results = []
    if isinstance(data, dict):
        if element_name in data:
            results.append(data[element_name])
        for v in data.values():
            sub = find_element_value(v, element_name)
            if isinstance(sub, list):
                results.extend(sub)
    elif isinstance(data, list):
        for item in data:
            sub = find_element_value(item, element_name)
            if isinstance(sub, list):
                results.extend(sub)
    if index is None:
        return results
    else:
        return results[index] if 0 <= index < len(results) else None

def _get_len_dossier():
    from pathlib import Path

    dossier = Path("../tools/scrap/data/")
    fichiers = [f for f in dossier.iterdir() if f.is_file()]

    print(f"Nombre de fichiers : {len(fichiers)}")
    return len(fichiers)

def get_all_values(name, mode):
    """
    Récupère toutes les valeurs numériques d'un attribut ou élément dans tous les fichiers de scrap/tools/scrap/data.
    """
    data_dir = os.path.join('scrap', 'tools', 'scrap', 'data')
    values = []
    for file in os.listdir(data_dir):
        if file.startswith('ads_') and file.endswith('.json'):
            file_path = os.path.join(data_dir, file)
            print(f"Lecture du fichier : {file_path}")
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
            if mode == 'attribute':
                vals = get_attribute_value(data, name)
            elif mode == 'element':
                vals = find_element_value(data, name)
            else:
                continue
            print(f"Valeurs extraites pour {name} ({mode}) : {vals}")
            if vals is None:
                continue
            for v in vals:
                # Si la valeur est une liste, on traite chaque élément
                if isinstance(v, list):
                    for item in v:
                        try:
                            if isinstance(item, str):
                                item = item.replace(',', '.').replace(' ', '')
                            num = float(item)
                            print(f"Valeur retenue (liste) : {num}")
                            values.append(num)
                        except (ValueError, TypeError):
                            print(f"Valeur ignorée (liste, non numérique) : {item}")
                            continue
                else:
                    try:
                        if isinstance(v, str):
                            v = v.replace(',', '.').replace(' ', '')
                        num = float(v)
                        print(f"Valeur retenue : {num}")
                        values.append(num)
                    except (ValueError, TypeError):
                        print(f"Valeur ignorée (non numérique) : {v}")
                        continue
    print(f"Valeurs finales retenues pour {name} ({mode}) : {values}")
    return values

def get_max(name, mode):
    vals = get_all_values(name, mode)
    if vals:
        return max(vals)
    return None

def get_min(name, mode):
    vals = get_all_values(name, mode)
    if vals:
        return min(vals)
    return None

def get_mean(name, mode):
    vals = get_all_values(name, mode)
    if vals:
        return sum(vals)/len(vals)
    return None

# Affichage des résultats pour test
if __name__ == '__main__':
    """print("Toutes les marques :", get_attribute_value(data, "brand"))
    print("Marque à l'index 1 :", get_attribute_value(data, "brand", index=1))

    print("Tous les store_id :", find_element_value(data, "owner"))
    print("store_id à l'index 0 :", find_element_value(data, "store_id", index=0))"""
    #_get_len_dossier()

    print("Max price attribute:", get_max("price", "element"))
    print("Min price attribute:", get_min("price", "attribute"))
    print("Mean price attribute:", get_mean("price", "attribute"))
    print("Max store_id element:", get_max("store_id", "element"))
