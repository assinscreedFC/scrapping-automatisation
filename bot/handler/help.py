from aiogram.types import Message
from scrap.jobs.fetch_ads import fetch_ads
from scrap.jobs.statistic import get_attribute_value, find_element_value
import json
import os

COMMANDS_HELP = [
    {
        "cmd": "/start",
        "usage": "/start",
        "desc": "Démarre le bot.",
        "example": None
    },
    {
        "cmd": "/help",
        "usage": "/help",
        "desc": "Affiche ce message d'aide.",
        "example": None
    },
    {
        "cmd": "/search",
        "usage": "/search <url> <nombre_de_pages>",
        "desc": "Lance le scraping sur l'URL donnée pour le nombre de pages indiqué.",
        "example": "/search https://www.leboncoin.fr/recherche?category=2 2"
    },
    {
        "cmd": "/extract",
        "usage": "/extract <attribute|element> <clé> [index]",
        "desc": "Extrait une valeur d'attribut ou d'élément depuis les fichiers ads_<n>.json générés.\n- attribute : recherche dans les attributs (ex : brand, model, price, etc.)\n- element : recherche une clé dans tout le JSON (ex : store_id, owner, etc.)\n- [index] (optionnel) : pour ne récupérer qu'une valeur précise dans la liste.",
        "example": "/extract attribute brand\n/extract element store_id 0"
    },
    {
        "cmd": "/description",
        "usage": "/description <url_annonce>",
        "desc": "Récupère la description d'une annonce précise à partir de son URL.",
        "example": "/description https://www.leboncoin.fr/ad/voitures/2997258439"
    }
]

ATTRIBUTES = [
    "brand : Marque du véhicule",
    "model : Modèle",
    "price : Prix",
    "u_car_brand : Marque (format alternatif)",
    "u_car_model : Modèle (format alternatif)",
    "horsepower, horse_power_din : Puissance",
    "vehicule_color : Couleur",
    "critair : Crit'Air",
    "estimated_parcel_weight, estimated_parcel_size : Poids, taille"
]

ELEMENTS = [
    "store_id : Identifiant du vendeur",
    "owner : Informations du vendeur",
    "attributes : Liste complète des attributs",
    "ad_id : Identifiant de l'annonce",
    "description : Description de l'annonce"
]

def generate_help_text():
    text = "<b>📌 Commandes disponibles :</b>\n"
    for cmd in COMMANDS_HELP:
        text += f"<b>{cmd['usage']}</b> : {cmd['desc']}\n"
        if cmd['example']:
            text += f"   Exemple : {cmd['example']}\n"
    text += "\n<b>Principaux attributes recherchables :</b>\n"
    for attr in ATTRIBUTES:
        text += f"- {attr}\n"
    text += "\n<b>Principaux elements recherchables :</b>\n"
    for el in ELEMENTS:
        text += f"- {el}\n"
    text += "\nPour toute question, contacte l'administrateur du bot."
    return text

async def help_cmd(message: Message):
    await message.answer(generate_help_text(), parse_mode="HTML")
