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

#### 🔧 **Filtrage**
```
/filter [min] [max] [ville]  # Filtre par prix et localisation
/modifier [critères]         # Modifie les données
```

#### 📋 **Aide**
```
/help                 # Aide générale
/help [commande]      # Aide spécifique
```

## 🏗 Architecture

```
scrapping-automatisation/
├── bot/                    # Bot Telegram
│   ├── handler/           # Gestionnaires de commandes
│   ├── config.py          # Configuration
│   └── data.json          # Données du bot
├── scrap/                 # Module de scraping
│   ├── analysis/          # Analyse et statistiques
│   ├── core/              # Parser et modèles
│   ├── infra/             # HTTP, proxy, logger
│   └── jobs/              # Tâches de scraping
├── main.py                # Point d'entrée
└── requirements.txt       # Dépendances
```

## 🔧 Technologies

- **Bot Framework** : Aiogram 3.x
- **Scraping** : Requests, BeautifulSoup
- **Analyse** : Pandas, NumPy
- **Visualisation** : Matplotlib
- **Données** : JSON, CSV
- **Proxy** : Pool de proxies rotatifs

## 📊 Exemples d'utilisation

### Analyse de marché immobilier
```bash
/search "https://www.leboncoin.fr/ventes_immobilieres"
/stats
/chart price
/filter 200000 500000 Paris
```

### Étude de marché automobile
```bash
/search "https://www.leboncoin.fr/voitures"
/chart brand
/chartimg ville
/stats
```

## 🚀 Fonctionnalités avancées

### 🔄 **Proxy Rotatif**
- Pool de proxies automatique
- Rotation intelligente
- Validation des proxies

### 📈 **Graphiques avancés**
- Histogrammes interactifs
- Graphiques en barres
- Export PNG haute qualité

### 🛡 **Gestion d'erreurs**
- Middleware global
- Messages d'erreur clairs
- Logs détaillés

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- **Issues** : [GitHub Issues](https://github.com/votre-username/votre-repo/issues)
- **Documentation** : `/help` dans le bot
- **Contact** : [@votre_username](https://t.me/votre_username)

## 🔄 Changelog

### v2.0.0 - Graphiques avancés
- ✅ Graphiques images PNG
- ✅ Analyse des villes (élément city)
- ✅ Gestion d'erreurs améliorée
- ✅ Interface utilisateur optimisée

### v1.0.0 - Version initiale
- ✅ Bot Telegram basique
- ✅ Scraping d'annonces
- ✅ Statistiques simples
- ✅ Filtrage de base

---

⭐ **N'oubliez pas de star ce projet si il vous est utile !** 