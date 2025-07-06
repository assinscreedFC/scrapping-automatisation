from aiogram.types import Message
from scrap.utils.cleanup import cleanup_ads_data, get_ads_files_count

async def cleanup_cmd(message: Message):
    """
    Commande: /cleanup - Supprime toutes les données de scraping
    """
    try:
        # Vérifier combien de fichiers il y a avant suppression
        files_count = get_ads_files_count()
        
        if files_count == 0:
            await message.reply("🗑️ Aucune donnée à supprimer.")
            return
        
        # Supprimer les données
        deleted_count = cleanup_ads_data()
        
        if deleted_count > 0:
            await message.reply(f"🗑️ {deleted_count} fichiers supprimés avec succès.")
        else:
            await message.reply("❌ Erreur lors de la suppression des données.")
            
    except Exception as e:
        await message.reply(f"❌ Erreur lors du nettoyage: {str(e)}")

async def cleanup_status_cmd(message: Message):
    """
    Commande: /cleanupstatus - Affiche le statut des données
    """
    try:
        files_count = get_ads_files_count()
        
        if files_count == 0:
            await message.reply("📊 Statut: Aucune donnée de scraping trouvée.")
        else:
            await message.reply(f"📊 Statut: {files_count} fichiers de données trouvés.\nUtilisez /cleanup pour les supprimer.")
            
    except Exception as e:
        await message.reply(f"❌ Erreur lors de la vérification: {str(e)}") 