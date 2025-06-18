from aiogram.types import Message
from bot.utils.modifierJson import modifier_fichier_json, FichierNonTrouveError, CleNonTrouveeError

async def modifier_data(message: Message):
    try:
        _, cle, nouvelle_valeur = message.text.split(maxsplit=2)
    except ValueError:
        await message.reply("Usage : /modifier <clé> <valeur>")
        return

    try:
        modifier_fichier_json("data.json", cle, nouvelle_valeur)
    except FichierNonTrouveError as e:
        await message.reply(str(e))
        return
    except CleNonTrouveeError as e:
        await message.reply(str(e))
        return

    await message.reply(f"Donnée modifiée : {cle} = {nouvelle_valeur}")
