"""
Module utilitaire pour nettoyer les données de scraping
"""

import os
import glob
import logging

logger = logging.getLogger(__name__)

def cleanup_ads_data():
    """
    Supprime tous les fichiers ads_*.json du répertoire de données
    """
    data_dir = os.path.join("scrap", "tools", "scrap", "data")
    
    if not os.path.exists(data_dir):
        logger.info("Répertoire de données n'existe pas, rien à nettoyer")
        return 0
    
    # Supprimer tous les fichiers ads_*.json
    pattern = os.path.join(data_dir, "ads_*.json")
    files_to_delete = glob.glob(pattern)
    
    deleted_count = 0
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            deleted_count += 1
            logger.info(f"Fichier supprimé: {file_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de {file_path}: {e}")
    
    logger.info(f"Nettoyage terminé: {deleted_count} fichiers supprimés")
    return deleted_count

def get_ads_files_count():
    """
    Retourne le nombre de fichiers ads_*.json dans le répertoire de données
    """
    data_dir = os.path.join("scrap", "tools", "scrap", "data")
    
    if not os.path.exists(data_dir):
        return 0
    
    pattern = os.path.join(data_dir, "ads_*.json")
    files = glob.glob(pattern)
    return len(files)

def cleanup_exports():
    """
    Supprime tous les fichiers du répertoire exports/
    """
    exports_dir = "exports"
    
    if not os.path.exists(exports_dir):
        logger.info("Répertoire exports n'existe pas, rien à nettoyer")
        return 0
    
    deleted_count = 0
    for file_path in os.listdir(exports_dir):
        full_path = os.path.join(exports_dir, file_path)
        if os.path.isfile(full_path):
            try:
                os.remove(full_path)
                deleted_count += 1
                logger.info(f"Fichier export supprimé: {full_path}")
            except Exception as e:
                logger.error(f"Erreur lors de la suppression de {full_path}: {e}")
    
    logger.info(f"Nettoyage des exports terminé: {deleted_count} fichiers supprimés")
    return deleted_count 