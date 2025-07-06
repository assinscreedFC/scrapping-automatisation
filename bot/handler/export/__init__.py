# Module d'exportation pour le bot Telegram 
import os

async def send_file(message, file, temp_path):
    await message.answer_document(document=file)
    os.unlink(temp_path)  # Suppression du fichier temporaire juste après l'envoi 