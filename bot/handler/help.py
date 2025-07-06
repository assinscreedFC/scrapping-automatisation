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
        "usage": "/search [url] [nombre_de_pages]",
        "desc": "Lance le scraping sur l'URL donnée pour le nombre de pages indiqué.",
        "example": "/search https://www.leboncoin.fr/recherche?category=2 2"
    },
    {
        "cmd": "/extract",
        "usage": "/extract [attribute|element] [clé] [index]",
        "desc": "Extrait une valeur d'attribut ou d'élément depuis les fichiers ads_[n].json générés.\n- attribute : recherche dans les attributs (ex : brand, model, price, etc.)\n- element : recherche une clé dans tout le JSON (ex : store_id, owner, etc.)\n- [index] (optionnel) : pour ne récupérer qu'une valeur précise dans la liste.",
        "example": "/extract attribute brand\n/extract element store_id 0"
    },
    {
        "cmd": "/description",
        "usage": "/description [url_annonce]",
        "desc": "Récupère la description d'une annonce précise à partir de son URL.",
        "example": "/description https://www.leboncoin.fr/ad/voitures/2997258439"
    },
    {
        "cmd": "/list_attributes_elements",
        "usage": "/list_attributes_elements",
        "desc": "Affiche tous les attributes et elements trouvés dans les fichiers d'annonces.",
        "example": "/list_attributes_elements"
    },
    {
        "cmd": "/list_attributes",
        "usage": "/list_attributes",
        "desc": "Affiche tous les attributes trouvés dans les fichiers d'annonces.",
        "example": "/list_attributes"
    },
    {
        "cmd": "/list_elements",
        "usage": "/list_elements",
        "desc": "Affiche tous les elements trouvés dans les fichiers d'annonces.",
        "example": "/list_elements"
    },
    {
        "cmd": "/max",
        "usage": "/max [attribute|element] [nom]",
        "desc": "Affiche la valeur maximale d'un attribut ou élément sur tous les fichiers.",
        "example": "/max attribute price"
    },
    {
        "cmd": "/min",
        "usage": "/min [attribute|element] [nom]",
        "desc": "Affiche la valeur minimale d'un attribut ou élément sur tous les fichiers.",
        "example": "/min element store_id"
    },
    {
        "cmd": "/mean",
        "usage": "/mean [attribute|element] [nom]",
        "desc": "Affiche la moyenne d'un attribut ou élément sur tous les fichiers.",
        "example": "/mean attribute price"
    },
    {
        "cmd": "/filter",
        "usage": "/filter [filtres]",
        "desc": "Filtre les annonces selon plusieurs critères combinables : prix min, prix max, ville (city), marque (brand), etc. Utilisez des guillemets pour les noms avec espaces.",
        "example": "/filter city=Paris\n/filter min=10000 max=20000\n/filter brand=Renault city=Lyon\n/filter brand=\"Land Rover\" city=\"New York\"\n/filter min=5000 max=15000 city=Marseille brand=Peugeot"
    },
    {
        "cmd": "/stats",
        "usage": "/stats",
        "desc": "Affiche les statistiques générales des données.",
        "example": "/stats"
    },
    {
        "cmd": "/chart",
        "usage": "/chart [type]",
        "desc": "Affiche un graphique textuel sur les annonces. Types disponibles : price, brand, location, summary.",
        "example": "/chart price\n/chart brand\n/chart location\n/chart summary"
    },
    {
        "cmd": "/chartimg",
        "usage": "/chartimg price",
        "desc": "Envoie un histogramme des prix sous forme d'image PNG.",
        "example": "/chartimg price"
    },
    {
        "cmd": "/chartimg",
        "usage": "/chartimg [type]",
        "desc": "Envoie un graphique en image PNG. Types disponibles : price, ville.",
        "example": "/chartimg price\n/chartimg ville"
    },
    {
        "cmd": "/export",
        "usage": "/export",
        "desc": "Affiche un menu pour exporter les données vers différents formats (JSON, CSV, Excel).",
        "example": "/export"
    },
    {
        "cmd": "/exportjson",
        "usage": "/exportjson",
        "desc": "Exporte directement les données en format JSON et les envoie dans la conversation.",
        "example": "/exportjson"
    },
    {
        "cmd": "/exportcsv",
        "usage": "/exportcsv",
        "desc": "Exporte directement les données en format CSV et les envoie dans la conversation.",
        "example": "/exportcsv"
    },
    {
        "cmd": "/exportexcel",
        "usage": "/exportexcel",
        "desc": "Exporte directement les données en format Excel avec plusieurs feuilles et les envoie dans la conversation.",
        "example": "/exportexcel"
    },
    {
        "cmd": "/exportstats",
        "usage": "/exportstats",
        "desc": "Affiche les statistiques détaillées des données avec un bouton pour les exporter.",
        "example": "/exportstats"
    },
    {
        "cmd": "/cleanup",
        "usage": "/cleanup",
        "desc": "Supprime toutes les données de scraping stockées.",
        "example": "/cleanup"
    },
    {
        "cmd": "/cleanupstatus",
        "usage": "/cleanupstatus",
        "desc": "Affiche le statut des données de scraping (nombre de fichiers).",
        "example": "/cleanupstatus"
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
    text += "\nPour toute question, contacte l'administrateur du bot."
    return text

async def help_cmd(message: Message):
    await message.answer(generate_help_text(), parse_mode="HTML")
