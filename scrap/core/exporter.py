import json
import csv
import pandas as pd
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

# Imports conditionnels pour Google Sheets
try:
    import gspread
    from google.oauth2.service_account import Credentials
    from google.auth.exceptions import GoogleAuthError
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False
    gspread = None
    Credentials = None
    GoogleAuthError = None

logger = logging.getLogger(__name__)

class DataExporter:
    """Classe pour exporter les données vers différents formats"""
    
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = output_dir
        self._ensure_output_dir()
        
    def _ensure_output_dir(self):
        """Crée le répertoire de sortie s'il n'existe pas"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def _get_timestamp(self) -> str:
        """Retourne un timestamp pour les noms de fichiers"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def export_to_json(self, data: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """Exporte les données vers un fichier JSON"""
        if filename is None:
            filename = f"export_{self._get_timestamp()}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Données exportées vers JSON: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Erreur lors de l'export JSON: {e}")
            raise
    
    def export_to_csv(self, data: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """Exporte les données vers un fichier CSV"""
        if filename is None:
            filename = f"export_{self._get_timestamp()}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            if not data:
                logger.warning("Aucune donnée à exporter")
                return filepath
                
            # Convertir en DataFrame pandas pour une meilleure gestion
            df = pd.DataFrame(data)
            
            # Aplatir les colonnes complexes (comme 'images', 'attributes')
            df_flat = self._flatten_dataframe(df)
            
            df_flat.to_csv(filepath, index=False, encoding='utf-8')
            
            logger.info(f"Données exportées vers CSV: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Erreur lors de l'export CSV: {e}")
            raise
    
    def export_to_excel(self, data: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """Exporte les données vers un fichier Excel"""
        if filename is None:
            filename = f"export_{self._get_timestamp()}.xlsx"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            if not data:
                logger.warning("Aucune donnée à exporter")
                return filepath
                
            # Convertir en DataFrame pandas
            df = pd.DataFrame(data)
            
            # Aplatir les colonnes complexes
            df_flat = self._flatten_dataframe(df)
            
            # Créer un writer Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Feuille principale avec données aplaties
                df_flat.to_excel(writer, sheet_name='Données', index=False)
                
                # Feuille avec données originales (si pas trop complexes)
                df_simple = self._simplify_dataframe(df)
                df_simple.to_excel(writer, sheet_name='Données_Originales', index=False)
                
                # Feuille de statistiques
                stats_df = self._create_stats_dataframe(data)
                stats_df.to_excel(writer, sheet_name='Statistiques', index=False)
            
            logger.info(f"Données exportées vers Excel: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Erreur lors de l'export Excel: {e}")
            raise
    
    def export_to_google_sheets(self, data: List[Dict[str, Any]], 
                               credentials_file: str = "credentials.json",
                               spreadsheet_name: Optional[str] = None) -> str:
        """Exporte les données vers Google Sheets"""
        if not GOOGLE_SHEETS_AVAILABLE:
            raise ImportError("gspread et google-auth ne sont pas installés. Installez-les avec: pip install gspread google-auth google-auth-oauthlib google-auth-httplib2")
        
        try:
            if not os.path.exists(credentials_file):
                raise FileNotFoundError(f"Fichier de credentials non trouvé: {credentials_file}")
            
            # Configuration des credentials Google
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            
            credentials = Credentials.from_service_account_file(credentials_file, scopes=scope)
            client = gspread.authorize(credentials)
            
            # Créer ou ouvrir le spreadsheet
            if spreadsheet_name is None:
                spreadsheet_name = f"Export_Scraping_{self._get_timestamp()}"
            
            try:
                spreadsheet = client.open(spreadsheet_name)
            except gspread.SpreadsheetNotFound:
                spreadsheet = client.create(spreadsheet_name)
            
            # Convertir les données
            df = pd.DataFrame(data)
            df_flat = self._flatten_dataframe(df)
            
            # Préparer les données pour Google Sheets
            headers = df_flat.columns.tolist()
            values = [headers] + df_flat.values.tolist()
            
            # Créer ou mettre à jour la feuille principale
            try:
                worksheet = spreadsheet.worksheet('Données')
                worksheet.clear()
            except gspread.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(title='Données', rows=1000, cols=50)
            
            # Mettre à jour les données
            worksheet.update(values)
            
            # Créer une feuille de statistiques
            stats_df = self._create_stats_dataframe(data)
            stats_values = [stats_df.columns.tolist()] + stats_df.values.tolist()
            
            try:
                stats_worksheet = spreadsheet.worksheet('Statistiques')
                stats_worksheet.clear()
            except gspread.WorksheetNotFound:
                stats_worksheet = spreadsheet.add_worksheet(title='Statistiques', rows=100, cols=20)
            
            stats_worksheet.update(stats_values)
            
            logger.info(f"Données exportées vers Google Sheets: {spreadsheet.url}")
            return spreadsheet.url
            
        except GoogleAuthError as e:
            logger.error(f"Erreur d'authentification Google: {e}")
            raise
        except Exception as e:
            logger.error(f"Erreur lors de l'export Google Sheets: {e}")
            raise
    
    def _flatten_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplatit un DataFrame avec des colonnes complexes"""
        df_flat = df.copy()
        
        # Traiter les colonnes complexes
        for col in df_flat.columns:
            if df_flat[col].dtype == 'object':
                # Vérifier si c'est une liste ou un dict
                sample_value = df_flat[col].dropna().iloc[0] if not df_flat[col].dropna().empty else None
                
                if isinstance(sample_value, list):
                    # Colonne de liste - prendre le premier élément ou la longueur
                    df_flat[f"{col}_count"] = df_flat[col].apply(lambda x: len(x) if isinstance(x, list) else 0)
                    df_flat[f"{col}_first"] = df_flat[col].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)
                    df_flat = df_flat.drop(columns=[col])
                
                elif isinstance(sample_value, dict):
                    # Colonne de dictionnaire - extraire les clés principales
                    if col == 'images':
                        df_flat[f"{col}_nb_images"] = df_flat[col].apply(
                            lambda x: x.get('nb_images', 0) if isinstance(x, dict) else 0
                        )
                        df_flat[f"{col}_thumb_url"] = df_flat[col].apply(
                            lambda x: x.get('thumb_url', '') if isinstance(x, dict) else ''
                        )
                        df_flat = df_flat.drop(columns=[col])
                    
                    elif col == 'attributes':
                        # Extraire les attributs importants
                        df_flat[f"{col}_brand"] = df_flat[col].apply(
                            lambda x: self._extract_attribute_value(x, 'brand') if isinstance(x, list) else None
                        )
                        df_flat[f"{col}_model"] = df_flat[col].apply(
                            lambda x: self._extract_attribute_value(x, 'model') if isinstance(x, list) else None
                        )
                        df_flat[f"{col}_mileage"] = df_flat[col].apply(
                            lambda x: self._extract_attribute_value(x, 'mileage') if isinstance(x, list) else None
                        )
                        df_flat[f"{col}_fuel"] = df_flat[col].apply(
                            lambda x: self._extract_attribute_value(x, 'fuel') if isinstance(x, list) else None
                        )
                        df_flat = df_flat.drop(columns=[col])
        
        return df_flat
    
    def _simplify_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Simplifie un DataFrame en gardant les colonnes principales"""
        # Garder seulement les colonnes simples
        simple_cols = []
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64', 'object']:
                sample_value = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
                if not isinstance(sample_value, (list, dict)):
                    simple_cols.append(col)
        
        return df[simple_cols]
    
    def _extract_attribute_value(self, attributes: List[Dict], key: str) -> Optional[str]:
        """Extrait une valeur d'attribut spécifique"""
        if not isinstance(attributes, list):
            return None
        
        for attr in attributes:
            if isinstance(attr, dict) and attr.get('key') == key:
                return attr.get('value')
        return None
    
    def _create_stats_dataframe(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Crée un DataFrame de statistiques"""
        if not data:
            return pd.DataFrame(columns=['Métrique', 'Valeur'])
        
        stats = {
            'Métrique': [],
            'Valeur': []
        }
        
        # Statistiques de base
        stats['Métrique'].extend(['Nombre total d\'annonces', 'Prix moyen', 'Prix minimum', 'Prix maximum'])
        
        total_ads = len(data)
        prices = [item.get('price_cents', 0) / 100 for item in data if item.get('price_cents')]
        
        stats['Valeur'].extend([
            total_ads,
            sum(prices) / len(prices) if prices else 0,
            min(prices) if prices else 0,
            max(prices) if prices else 0
        ])
        
        # Statistiques par catégorie
        categories = {}
        for item in data:
            cat = item.get('category_name', 'Inconnue')
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in categories.items():
            stats['Métrique'].append(f'Catégorie: {cat}')
            stats['Valeur'].append(count)
        
        return pd.DataFrame(stats)
    
    def export_all_formats(self, data: List[Dict[str, Any]], 
                          base_filename: Optional[str] = None) -> Dict[str, str]:
        """Exporte les données vers tous les formats disponibles"""
        if base_filename is None:
            base_filename = f"export_{self._get_timestamp()}"
        
        results = {}
        
        try:
            # Export JSON
            results['json'] = self.export_to_json(data, f"{base_filename}.json")
        except Exception as e:
            logger.error(f"Erreur export JSON: {e}")
            results['json'] = None
        
        try:
            # Export CSV
            results['csv'] = self.export_to_csv(data, f"{base_filename}.csv")
        except Exception as e:
            logger.error(f"Erreur export CSV: {e}")
            results['csv'] = None
        
        try:
            # Export Excel
            results['excel'] = self.export_to_excel(data, f"{base_filename}.xlsx")
        except Exception as e:
            logger.error(f"Erreur export Excel: {e}")
            results['excel'] = None
        
        return results
