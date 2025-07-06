#!/usr/bin/env python3
"""
Système d'exportation et de téléchargement de données
Permet d'exporter les données vers JSON, CSV, Excel et Google Sheets
"""

import json
import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

# Ajouter le répertoire scrap au path
sys.path.append(str(Path(__file__).parent / "scrap"))

from scrap.core.exporter import DataExporter

# Import conditionnel pour le serveur web
try:
    from scrap.core.download_server import DownloadServer
    DOWNLOAD_SERVER_AVAILABLE = True
except ImportError:
    DOWNLOAD_SERVER_AVAILABLE = False
    DownloadServer = None

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_data_from_file(filepath: str) -> list:
    """Charge les données depuis un fichier JSON ou utilise le répertoire par défaut"""
    try:
        # Si aucun fichier spécifié, utiliser le répertoire par défaut
        if not filepath:
            from scrap.analysis.filters import load_ads_data
            data = load_ads_data()
            logger.info(f"Données chargées depuis le répertoire par défaut: {len(data)} éléments")
            return data
        
        # Sinon, charger le fichier spécifié
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            logger.info(f"Données chargées: {len(data)} éléments")
            return data
        else:
            logger.warning("Les données ne sont pas une liste, conversion en liste")
            return [data]
            
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé: {filepath}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de décodage JSON: {e}")
        return []
    except Exception as e:
        logger.error(f"Erreur lors du chargement: {e}")
        return []

def export_data(data: list, format_type: str = "all", filename: Optional[str] = None) -> dict:
    """Exporte les données vers le format spécifié"""
    exporter = DataExporter()
    
    try:
        if format_type == "json":
            filepath = exporter.export_to_json(data, filename)
            return {"json": filepath}
        elif format_type == "csv":
            filepath = exporter.export_to_csv(data, filename)
            return {"csv": filepath}
        elif format_type == "excel":
            filepath = exporter.export_to_excel(data, filename)
            return {"excel": filepath}
        elif format_type == "all":
            return exporter.export_all_formats(data, filename)
        else:
            logger.error(f"Format non supporté: {format_type}")
            return {}
            
    except Exception as e:
        logger.error(f"Erreur lors de l'export: {e}")
        return {}

def start_download_server(host: str = "0.0.0.0", port: int = 5000):
    """Démarre le serveur de téléchargement"""
    if not DOWNLOAD_SERVER_AVAILABLE:
        logger.error("Serveur web non disponible. Installez Flask avec: pip install flask flask-cors")
        return
        
    try:
        server = DownloadServer(host=host, port=port)
        logger.info(f"Serveur de téléchargement démarré sur http://{host}:{port}")
        logger.info("Appuyez sur Ctrl+C pour arrêter le serveur")
        server.start()
    except KeyboardInterrupt:
        logger.info("Arrêt du serveur...")
    except Exception as e:
        logger.error(f"Erreur lors du démarrage du serveur: {e}")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Système d'exportation et de téléchargement de données",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  # Exporter ads_1.json vers tous les formats
  python export_system.py --file ads_1.json --export all
  
  # Exporter vers CSV seulement
  python export_system.py --file ads_1.json --export csv
  
  # Démarrer le serveur web
  python export_system.py --server
  
  # Exporter et démarrer le serveur
  python export_system.py --file ads_1.json --export all --server
        """
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Fichier JSON à exporter (optionnel, utilise le répertoire par défaut si non spécifié)'
    )
    
    parser.add_argument(
        '--export', '-e',
        choices=['json', 'csv', 'excel', 'all'],
        default='all',
        help='Format d\'export (défaut: all)'
    )
    
    parser.add_argument(
        '--filename', '-n',
        type=str,
        help='Nom de base du fichier d\'export (sans extension)'
    )
    
    parser.add_argument(
        '--server', '-s',
        action='store_true',
        help='Démarrer le serveur web de téléchargement'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Adresse du serveur (défaut: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=5000,
        help='Port du serveur (défaut: 5000)'
    )
    
    parser.add_argument(
        '--google-sheets',
        action='store_true',
        help='Exporter vers Google Sheets (nécessite credentials.json)'
    )
    
    parser.add_argument(
        '--credentials',
        type=str,
        default='credentials.json',
        help='Fichier de credentials Google (défaut: credentials.json)'
    )
    
    args = parser.parse_args()
    
    # Si aucun argument n'est fourni, afficher l'aide
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # Charger et exporter les données
    if args.file:
        logger.info(f"Chargement du fichier: {args.file}")
        data = load_data_from_file(args.file)
    else:
        logger.info("Chargement depuis le répertoire par défaut")
        data = load_data_from_file("")
    
    if not data:
        logger.error("Aucune donnée à exporter")
        return
    
    logger.info(f"Export vers le format: {args.export}")
    results = export_data(data, args.export, args.filename)
    
    if results:
        logger.info("Export réussi!")
        for format_type, filepath in results.items():
            if filepath:
                logger.info(f"  {format_type.upper()}: {filepath}")
            else:
                logger.warning(f"  {format_type.upper()}: Échec")
    
    # Export Google Sheets si demandé
    if args.google_sheets:
        try:
            exporter = DataExporter()
            url = exporter.export_to_google_sheets(data, args.credentials)
            logger.info(f"Google Sheets: {url}")
        except Exception as e:
            logger.error(f"Erreur export Google Sheets: {e}")
    
    # Démarrer le serveur si demandé
    if args.server:
        if not DOWNLOAD_SERVER_AVAILABLE:
            logger.error("Serveur web non disponible. Installez Flask avec: pip install flask flask-cors")
            return
        start_download_server(args.host, args.port)

if __name__ == "__main__":
    main() 