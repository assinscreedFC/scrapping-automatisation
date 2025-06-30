from aiogram.types import Message, BufferedInputFile
from scrap.jobs.statistic import get_attribute_value, find_element_value, get_max, get_min, get_mean
from scrap.jobs.fetch_ads import fetch_description_ads
import json
import os
from collections import Counter, defaultdict
import io

async def extract_cmd(message: Message):
    if not message.text:
        await message.reply("Usage : /extract <attribute|element> <clé> [index]")
        return
    try:
        parts = message.text.split(maxsplit=3)
        if len(parts) == 4:
            _, mode, param, index = parts
            index = int(index)
        else:
            _, mode, param = parts
            index = None
    except ValueError:
        await message.reply("Usage : /extract <attribute|element> <clé> [index]")
        return
    data_dir = os.path.join("scrap", "tools", "scrap", "data")
    if not os.path.exists(data_dir):
        await message.reply("Aucune donnée à extraire. Lancez d'abord /search.")
        return
    results = []
    for file in os.listdir(data_dir):
        if file.startswith("ads_") and file.endswith(".json"):
            file_path = os.path.join(data_dir, file)
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
            if mode == "attribute":
                res = get_attribute_value(data, param, index)
            elif mode == "element":
                res = find_element_value(data, param, index)
            else:
                await message.reply("Mode inconnu. Utilisez 'attribute' ou 'element'.")
                return
            results.append({file: res})
    if not results:
        await message.reply("Aucun fichier ads_<nbr>.json trouvé.")
        return
    # On limite la taille du message pour Telegram
    msg = json.dumps(results, ensure_ascii=False)
    if len(msg) > 4000:
        msg = msg[:3990] + "... (résultat tronqué)"
    await message.reply(f"Résultat : {msg}")

async def extract_description_cmd(message: Message):
    if not message.text:
        await message.reply("Usage : /description <url_annonce>")
        return
    try:
        _, url = message.text.split(maxsplit=1)
    except ValueError:
        await message.reply("Usage : /description <url_annonce>")
        return
    try:
        description = fetch_description_ads(url)
        await message.reply(f"Description : {description}")
    except Exception as e:
        await message.reply(f"Erreur lors de la récupération : {e}")

async def list_attributes_elements_cmd(message: Message):
    data_dir = os.path.join("scrap", "tools", "scrap", "data")
    if not os.path.exists(data_dir):
        await message.reply("Aucune donnée à analyser. Lancez d'abord /search.")
        return
    attribute_set = set()
    element_set = set()
    for file in os.listdir(data_dir):
        if file.startswith("ads_") and file.endswith(".json"):
            file_path = os.path.join(data_dir, file)
            with open(file_path, encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception:
                    continue
                # Si le fichier contient une liste d'annonces
                if isinstance(data, list):
                    for ad in data:
                        if isinstance(ad, dict):
                            element_set.update(ad.keys())
                            if "attributes" in ad and isinstance(ad["attributes"], list):
                                for attr in ad["attributes"]:
                                    if isinstance(attr, dict) and "key" in attr:
                                        attribute_set.add(attr["key"])
                elif isinstance(data, dict):
                    element_set.update(data.keys())
                    if "attributes" in data and isinstance(data["attributes"], list):
                        for attr in data["attributes"]:
                            if isinstance(attr, dict) and "key" in attr:
                                attribute_set.add(attr["key"])
    msg = "<b>Attributes trouvés :</b>\n"
    for k in sorted(attribute_set):
        msg += f"- {k}\n"
    msg += "\n<b>Elements trouvés :</b>\n"
    for k in sorted(element_set):
        msg += f"- {k}\n"
    if len(msg) > 4000:
        msg = msg[:3990] + "... (résultat tronqué)"
    await message.reply(msg, parse_mode="HTML")

async def list_attributes_cmd(message: Message):
    data_dir = os.path.join("scrap", "tools", "scrap", "data")
    if not os.path.exists(data_dir):
        await message.reply("Aucune donnée à analyser. Lancez d'abord /search.")
        return
    attribute_set = set()
    for file in os.listdir(data_dir):
        if file.startswith("ads_") and file.endswith(".json"):
            file_path = os.path.join(data_dir, file)
            with open(file_path, encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception:
                    continue
                if isinstance(data, list):
                    for ad in data:
                        if isinstance(ad, dict) and "attributes" in ad and isinstance(ad["attributes"], list):
                            for attr in ad["attributes"]:
                                if isinstance(attr, dict) and "key" in attr:
                                    attribute_set.add(attr["key"])
                elif isinstance(data, dict) and "attributes" in data and isinstance(data["attributes"], list):
                    for attr in data["attributes"]:
                        if isinstance(attr, dict) and "key" in attr:
                            attribute_set.add(attr["key"])
    msg = "<b>Attributes trouvés :</b>\n"
    for k in sorted(attribute_set):
        msg += f"- {k}\n"
    if len(msg) > 4000:
        msg = msg[:3990] + "... (résultat tronqué)"
    await message.reply(msg, parse_mode="HTML")

async def list_elements_cmd(message: Message):
    data_dir = os.path.join("scrap", "tools", "scrap", "data")
    if not os.path.exists(data_dir):
        await message.reply("Aucune donnée à analyser. Lancez d'abord /search.")
        return
    element_levels = dict()
    def collect_keys(obj, level=0):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k not in element_levels or level < element_levels[k]:
                    element_levels[k] = level
                collect_keys(v, level+1)
        elif isinstance(obj, list):
            for item in obj:
                collect_keys(item, level)
    for file in os.listdir(data_dir):
        if file.startswith("ads_") and file.endswith(".json"):
            file_path = os.path.join(data_dir, file)
            with open(file_path, encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception:
                    continue
                collect_keys(data)
    msg = "<b>Elements trouvés :</b>\n"
    for k in sorted(element_levels, key=lambda x: (element_levels[x], x)):
        msg += f"{'\t'*4*element_levels[k]}- {k}\n"
    if len(msg) > 4000:
        msg = msg[:3990] + "... (résultat tronqué)"
    await message.reply(msg, parse_mode="HTML")

async def max_cmd(message: Message):
    if not message.text:
        await message.reply("Usage : /max [attribute|element] [nom]")
        return
    try:
        _, mode, nom = message.text.split(maxsplit=2)
    except ValueError:
        await message.reply("Usage : /max [attribute|element] [nom]")
        return
    if mode not in ("attribute", "element"):
        await message.reply("Mode inconnu. Utilisez 'attribute' ou 'element'.")
        return
    val = get_max(nom, mode)
    if val is not None:
        await message.reply(f"Max de {nom} ({mode}) : {val}")
    else:
        await message.reply(f"Aucune valeur trouvée pour {nom} ({mode})")

async def min_cmd(message: Message):
    if not message.text:
        await message.reply("Usage : /min [attribute|element] [nom]")
        return
    try:
        _, mode, nom = message.text.split(maxsplit=2)
    except ValueError:
        await message.reply("Usage : /min [attribute|element] [nom]")
        return
    if mode not in ("attribute", "element"):
        await message.reply("Mode inconnu. Utilisez 'attribute' ou 'element'.")
        return
    val = get_min(nom, mode)
    if val is not None:
        await message.reply(f"Min de {nom} ({mode}) : {val}")
    else:
        await message.reply(f"Aucune valeur trouvée pour {nom} ({mode})")

async def mean_cmd(message: Message):
    if not message.text:
        await message.reply("Usage : /mean [attribute|element] [nom]")
        return
    try:
        _, mode, nom = message.text.split(maxsplit=2)
    except ValueError:
        await message.reply("Usage : /mean [attribute|element] [nom]")
        return
    if mode not in ("attribute", "element"):
        await message.reply("Mode inconnu. Utilisez 'attribute' ou 'element'.")
        return
    val = get_mean(nom, mode)
    if val is not None:
        await message.reply(f"Moyenne de {nom} ({mode}) : {val}")
    else:
        await message.reply(f"Aucune valeur trouvée pour {nom} ({mode})")

async def histogram_cmd(message: Message):
    if not message.text:
        await message.reply("Usage : /histogram <attribute|element> <clé> [index]")
        return
    try:
        parts = message.text.split(maxsplit=3)
        if len(parts) == 4:
            _, mode, param, index = parts
            index = int(index)
        else:
            _, mode, param = parts
            index = None
    except ValueError:
        await message.reply("Usage : /histogram <attribute|element> <clé> [index]")
        return
    data_dir = os.path.join("scrap", "tools", "scrap", "data")
    if not os.path.exists(data_dir):
        await message.reply("Aucune donnée à analyser. Lancez d'abord /search.")
        return
    results = []
    for file in os.listdir(data_dir):
        if file.startswith("ads_") and file.endswith(".json"):
            file_path = os.path.join(data_dir, file)
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
            if mode == "attribute":
                res = get_attribute_value(data, param, index)
            elif mode == "element":
                res = find_element_value(data, param, index)
            else:
                await message.reply("Mode inconnu. Utilisez 'attribute' ou 'element'.")
                return
            results.append({file: res})
    if not results:
        await message.reply("Aucun fichier ads_<nbr>.json trouvé.")
        return
    # On génère le graphique
    buf = io.BytesIO()
    # ... (code pour générer le graphique et l'écrire dans buf)
    buf.seek(0)
    photo = BufferedInputFile(buf.read(), filename="histogramme.png")
    await message.answer_photo(photo, caption="Histogramme des prix") 