import json

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
            results.extend(get_attribute_value(v, attribute_key))
    elif isinstance(data, list):
        for item in data:
            results.extend(get_attribute_value(item, attribute_key))
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
            results.extend(find_element_value(v, element_name))
    elif isinstance(data, list):
        for item in data:
            results.extend(find_element_value(item, element_name))
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

#def get_max():

#def get_min():

#def get_mean():

# Affichage des résultats pour test
if __name__ == '__main__':
    """print("Toutes les marques :", get_attribute_value(data, "brand"))
    print("Marque à l'index 1 :", get_attribute_value(data, "brand", index=1))

    print("Tous les store_id :", find_element_value(data, "owner"))
    print("store_id à l'index 0 :", find_element_value(data, "store_id", index=0))"""
    _get_len_dossier()
