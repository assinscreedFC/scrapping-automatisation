import json
import os
import tempfile
import logging
from typing import List, Dict, Any, Optional
from aiogram.types import Message, FSInputFile
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pandas as pd
from datetime import datetime

# Ajouter le répertoire parent au path pour importer les modules
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from scrap.core.exporter import DataExporter
from scrap.analysis.filters import load_ads_data

logger = logging.getLogger(__name__)

class BotExporter:
    """Classe pour exporter et envoyer des fichiers via Telegram"""
    
    def __init__(self):
        self.exporter = DataExporter()
        
    def load_data_from_files(self, pattern: str = "ads_*.json") -> List[Dict[str, Any]]:
        """Charge les données depuis les fichiers ads_*.json en utilisant le même système que /stats"""
        # Utiliser la même fonction que /stats pour charger toutes les données
        data = load_ads_data()
        logger.info(f"Total des données chargées: {len(data)} éléments")
        return data
    
    async def export_and_send_json(self, message: Message, data: List[Dict[str, Any]], filename: Optional[str] = None) -> bool:
        """Exporte et envoie un fichier JSON"""
        try:
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                temp_path = f.name
            
            # Envoyer le fichier
            file_name = filename or f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            file = FSInputFile(temp_path, filename=file_name)
            
            await message.answer_document(
                document=file,
                caption=f"📄 Export JSON\n📊 {len(data)} annonces\n📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )
            
            # Nettoyer le fichier temporaire
            os.unlink(temp_path)
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export JSON: {e}")
            await message.answer(f"❌ Erreur lors de l'export JSON: {e}")
            return False
    
    async def export_and_send_csv(self, message: Message, data: List[Dict[str, Any]], filename: Optional[str] = None) -> bool:
        """Exporte et envoie un fichier CSV"""
        try:
            if not data:
                await message.answer("❌ Aucune donnée à exporter")
                return False
            
            # Convertir en DataFrame et aplatir
            df = pd.DataFrame(data)
            df_flat = self.exporter._flatten_dataframe(df)
            
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
                df_flat.to_csv(f, index=False, encoding='utf-8')
                temp_path = f.name
            
            # Envoyer le fichier
            file_name = filename or f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            file = FSInputFile(temp_path, filename=file_name)
            
            await message.answer_document(
                document=file,
                caption=f"📊 Export CSV\n📈 {len(data)} annonces\n📋 {len(df_flat.columns)} colonnes\n📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )
            
            # Nettoyer le fichier temporaire
            os.unlink(temp_path)
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export CSV: {e}")
            await message.answer(f"❌ Erreur lors de l'export CSV: {e}")
            return False
    
    async def export_and_send_excel(self, message: Message, data: List[Dict[str, Any]], filename: Optional[str] = None) -> bool:
        """Exporte et envoie un fichier Excel"""
        try:
            if not data:
                await message.answer("❌ Aucune donnée à exporter")
                return False
            
            # Convertir en DataFrame
            df = pd.DataFrame(data)
            df_flat = self.exporter._flatten_dataframe(df)
            df_simple = self.exporter._simplify_dataframe(df)
            stats_df = self.exporter._create_stats_dataframe(data)
            
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
                temp_path = f.name
            
            # Écrire le fichier Excel
            with pd.ExcelWriter(temp_path, engine='openpyxl') as writer:
                df_flat.to_excel(writer, sheet_name='Données', index=False)
                df_simple.to_excel(writer, sheet_name='Données_Originales', index=False)
                stats_df.to_excel(writer, sheet_name='Statistiques', index=False)
            
            # Envoyer le fichier
            file_name = filename or f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file = FSInputFile(temp_path, filename=file_name)
            
            await message.answer_document(
                document=file,
                caption=f"📈 Export Excel\n📊 {len(data)} annonces\n📋 {len(df_flat.columns)} colonnes\n📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )
            
            # Nettoyer le fichier temporaire
            os.unlink(temp_path)
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export Excel: {e}")
            await message.answer(f"❌ Erreur lors de l'export Excel: {e}")
            return False
    
    async def export_all_formats(self, message: Message, data: List[Dict[str, Any]], filename: Optional[str] = None) -> bool:
        """Exporte et envoie tous les formats"""
        try:
            if not data:
                await message.answer("❌ Aucune donnée à exporter")
                return False
            
            # Message de progression
            progress_msg = await message.answer("🔄 Export en cours...")
            
            success_count = 0
            total_formats = 3
            
            # Export JSON
            if await self.export_and_send_json(message, data, filename):
                success_count += 1
            
            # Export CSV
            if await self.export_and_send_csv(message, data, filename):
                success_count += 1
            
            # Export Excel
            if await self.export_and_send_excel(message, data, filename):
                success_count += 1
            
            # Message de résumé
            await progress_msg.edit_text(
                f"✅ Export terminé !\n"
                f"📊 {len(data)} annonces exportées\n"
                f"📁 {success_count}/{total_formats} formats envoyés\n"
                f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )
            
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export multiple: {e}")
            await message.answer(f"❌ Erreur lors de l'export: {e}")
            return False

# Instance globale
bot_exporter = BotExporter()

async def export_cmd(message: Message):
    """Commande principale d'export"""
    try:
        # Charger les données
        data = bot_exporter.load_data_from_files()
        
        if not data:
            await message.answer("❌ Aucune donnée trouvée. Utilisez d'abord /search pour récupérer des annonces.")
            return
        
        # Créer les boutons pour choisir le format
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📄 JSON", callback_data="export_json"),
                InlineKeyboardButton(text="📊 CSV", callback_data="export_csv"),
                InlineKeyboardButton(text="📈 Excel", callback_data="export_excel")
            ],
            [InlineKeyboardButton(text="📁 Tous les formats", callback_data="export_all")]
        ])
        
        await message.answer(
            f"📊 <b>Export des données</b>\n\n"
            f"📈 {len(data)} annonces trouvées\n"
            f"📅 Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"Choisissez le format d'export :",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"Erreur dans export_cmd: {e}")
        await message.answer(f"❌ Erreur: {e}")

async def export_callback(callback: types.CallbackQuery):
    """Gère les callbacks d'export"""
    try:
        # Charger les données
        data = bot_exporter.load_data_from_files()
        
        if not data:
            await callback.answer("❌ Aucune donnée trouvée")
            return
        
        # Traiter selon le format choisi
        if callback.data == "export_json":
            await callback.message.edit_text("🔄 Export JSON en cours...")
            success = await bot_exporter.export_and_send_json(callback.message, data)
            
        elif callback.data == "export_csv":
            await callback.message.edit_text("🔄 Export CSV en cours...")
            success = await bot_exporter.export_and_send_csv(callback.message, data)
            
        elif callback.data == "export_excel":
            await callback.message.edit_text("🔄 Export Excel en cours...")
            success = await bot_exporter.export_and_send_excel(callback.message, data)
            
        elif callback.data == "export_all":
            await callback.message.edit_text("🔄 Export de tous les formats en cours...")
            success = await bot_exporter.export_all_formats(callback.message, data)
        
        if success:
            await callback.answer("✅ Export réussi !")
        else:
            await callback.answer("❌ Erreur lors de l'export")
            
    except Exception as e:
        logger.error(f"Erreur dans export_callback: {e}")
        await callback.answer(f"❌ Erreur: {e}")

async def export_json_cmd(message: Message):
    """Commande pour exporter en JSON seulement"""
    try:
        data = bot_exporter.load_data_from_files()
        if data:
            await bot_exporter.export_and_send_json(message, data)
        else:
            await message.answer("❌ Aucune donnée trouvée")
    except Exception as e:
        await message.answer(f"❌ Erreur: {e}")

async def export_csv_cmd(message: Message):
    """Commande pour exporter en CSV seulement"""
    try:
        data = bot_exporter.load_data_from_files()
        if data:
            await bot_exporter.export_and_send_csv(message, data)
        else:
            await message.answer("❌ Aucune donnée trouvée")
    except Exception as e:
        await message.answer(f"❌ Erreur: {e}")

async def export_excel_cmd(message: Message):
    """Commande pour exporter en Excel seulement"""
    try:
        data = bot_exporter.load_data_from_files()
        if data:
            await bot_exporter.export_and_send_excel(message, data)
        else:
            await message.answer("❌ Aucune donnée trouvée")
    except Exception as e:
        await message.answer(f"❌ Erreur: {e}")

async def export_stats_cmd(message: Message):
    """Commande pour afficher les statistiques des données"""
    try:
        data = bot_exporter.load_data_from_files()
        
        if not data:
            await message.answer("❌ Aucune donnée trouvée")
            return
        
        # Calculer les statistiques
        total_ads = len(data)
        prices = [item.get('price_cents', 0) / 100 for item in data if item.get('price_cents')]
        
        stats_text = f"📊 <b>Statistiques des données</b>\n\n"
        stats_text += f"📈 Nombre total d'annonces: {total_ads}\n"
        
        if prices:
            stats_text += f"💰 Prix moyen: {sum(prices) / len(prices):.0f}€\n"
            stats_text += f"💰 Prix minimum: {min(prices):.0f}€\n"
            stats_text += f"💰 Prix maximum: {max(prices):.0f}€\n"
        
        # Statistiques par catégorie
        categories = {}
        for item in data:
            cat = item.get('category_name', 'Inconnue')
            categories[cat] = categories.get(cat, 0) + 1
        
        stats_text += f"\n📂 Répartition par catégorie:\n"
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_ads) * 100
            stats_text += f"  • {cat}: {count} ({percentage:.1f}%)\n"
        
        # Bouton pour exporter
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📁 Exporter les données", callback_data="export_all")]
        ])
        
        await message.answer(stats_text, reply_markup=keyboard, parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"Erreur dans export_stats_cmd: {e}")
        await message.answer(f"❌ Erreur: {e}") 