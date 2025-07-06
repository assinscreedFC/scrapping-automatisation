from aiogram.types import Message
from scrap.jobs.fetch_ads import fetch_ads
import os
import glob

async def search_cmd(message: Message):
    if not message.text:
        await message.reply("Usage : /search <url> <nombre_de_pages>")
        return
    
    try:
        _, url, page = message.text.split(maxsplit=2)
        page_int = int(page)
    except ValueError:
        await message.reply("Usage : /search <url> <nombre_de_pages>")
        return
    
    # Supprimer les anciennes données avant de commencer le nouveau scraping
    data_dir = os.path.join("scrap", "tools", "scrap", "data")
    if os.path.exists(data_dir):
        # Supprimer tous les fichiers ads_*.json
        pattern = os.path.join(data_dir, "ads_*.json")
        files_to_delete = glob.glob(pattern)
        
        if files_to_delete:
            deleted_count = 0
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"Erreur lors de la suppression de {file_path}: {e}")
            
            await message.reply(f"🗑️ {deleted_count} anciens fichiers supprimés. Début du nouveau scraping...")
        else:
            await message.reply("🔄 Début du scraping...")
    else:
        await message.reply("🔄 Création du répertoire de données et début du scraping...")
    
    # Lancer le scraping
    count = fetch_ads(url, page_int)
    if count:
        await message.reply(f"✅ Recherche terminée : {count} annonces trouvées pour {page_int} pages sur {url}")
    else:
        await message.reply("❌ Aucune annonce trouvée. Vérifie l'URL ou réessaie plus tard.") 