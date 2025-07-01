# 🤖 Bot Telegram - Scraping & Analyse d'Annonces

Un bot Telegram intelligent pour scraper, analyser et visualiser des annonces (ex: Leboncoin) avec des graphiques et statistiques avancées.

## 🚀 Fonctionnalités

### 📊 **Analyse & Statistiques**
- **Statistiques des prix** : min, max, moyenne, médiane
- **Distribution des marques** : top des marques les plus populaires
- **Analyse géographique** : répartition par villes
- **Filtrage avancé** : par prix, localisation, critères personnalisés

### 📈 **Visualisations**
- **Graphiques textuels** : histogrammes et barres en ASCII
- **Graphiques images** : histogrammes PNG envoyés directement sur Telegram
- **Graphiques interactifs** : prix et villes avec matplotlib

### 🔍 **Extraction & Filtrage**
- **Extraction robuste** : gestion des éléments et attributs JSON
- **Filtres dynamiques** : prix, localisation, mots-clés
- **Export de données** : JSON, CSV, formats personnalisés

## 🛠 Installation

### Prérequis
```bash
Python 3.8+
pip
```

### Installation
```bash
# Clone le repository
git clone <votre-repo>
cd scrapping-automatisation

# Installe les dépendances
pip install -r requirements.txt

# Configure le bot
cp bot/config.py.example bot/config.py
# Édite bot/config.py avec votre token Telegram
```

## 📋 Configuration

### Token Telegram
1. Créez un bot via [@BotFather](https://t.me/botfather)
2. Copiez le token dans `bot/config.py`
3. Lancez le bot : `python main.py`

### Variables d'environnement
```bash
TELEGRAM_TOKEN=votre_token_ici
```

## 🎯 Utilisation

### Commandes principales

#### 🔍 **Recherche & Extraction**
```
/search [url]          # Scrape une URL d'annonces
/extract [attribut]    # Extrait un attribut spécifique
/list_attributes       # Liste tous les attributs disponibles
/list_elements         # Liste tous les éléments disponibles
```

#### 📊 **Statistiques**
```
/stats                 # Statistiques générales
/min [attribut]        # Valeur minimale
/max [attribut]        # Valeur maximale
/mean [attribut]       # Valeur moyenne
```

#### 📈 **Graphiques**
```
/chart price           # Histogramme des prix (texte)
/chart brand           # Top des marques (texte)
/chart location        # Top des localisations (texte)
/chart summary         # Résumé complet (texte)

/chartimg price        # Histogramme des prix (image PNG)
/chartimg ville        # Top des villes (image PNG)
```

#### 📋 **Aide**
```