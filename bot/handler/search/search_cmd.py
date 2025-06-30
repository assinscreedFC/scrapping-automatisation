from aiogram.types import Message
from scrap.jobs.fetch_ads import fetch_ads

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
    count = fetch_ads(url, page_int)
    if count:
        await message.reply(f"Recherche terminée : {count} annonces trouvées pour {page_int} pages sur {url}")
    else:
        await message.reply("Aucune annonce trouvée. Vérifie l'URL ou réessaie plus tard.") 