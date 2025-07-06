from bot.handler.start import start_cmd
from bot.handler.help import help_cmd
from aiogram.filters import Command
from bot.handler.search.search_cmd import search_cmd
from bot.handler.extract.extract_cmd import extract_cmd, extract_description_cmd, list_attributes_elements_cmd, list_attributes_cmd, list_elements_cmd, max_cmd, min_cmd, mean_cmd
from bot.handler.filter.filter_cmd import filter_cmd, stats_cmd, chart_cmd, chart_img_cmd
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class ErrorHandlerMiddleware:
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except Exception as e:
            # Log l'erreur côté serveur
            print(f"[ERREUR] {type(e).__name__}: {e}")
            if isinstance(event, types.Message):
                await event.reply("❌ Une erreur inattendue est survenue. Merci de réessayer ou de contacter l'administrateur.")
            # On peut aussi logger dans un fichier ici si besoin
            return None

async def welcome_cmd(message: types.Message):
    """
    Commande de démarrage avec bouton d'aide
    """
    welcome_text = """
🤖 <b>Bienvenue sur le Bot de Scraping & Analyse d'Annonces !</b>

Ce bot vous permet de :
• 🔍 Scraper des annonces (Leboncoin, etc.)
• 📊 Analyser les données (prix, marques, villes)
• 📈 Générer des graphiques
• 🔧 Filtrer selon vos critères

Cliquez sur le bouton ci-dessous pour voir toutes les commandes disponibles :
"""
    
    # Créer le bouton d'aide
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Aide & Commandes", callback_data="show_help")]
    ])
    
    await message.reply(welcome_text, reply_markup=keyboard)

async def help_callback(callback: types.CallbackQuery):
    """
    Gère le clic sur le bouton d'aide
    """
    from bot.handler.help import generate_help_text
    help_text = generate_help_text()
    await callback.message.answer(help_text, parse_mode="HTML")
    await callback.answer()

def register_handlers(dp):
    dp.message.middleware(ErrorHandlerMiddleware())
    dp.message.register(welcome_cmd, Command("start"))
    dp.message.register(help_cmd, Command("help"))
    dp.callback_query.register(help_callback, lambda c: c.data == "show_help")
    dp.message.register(search_cmd, Command("search"))
    dp.message.register(extract_cmd, Command("extract"))
    dp.message.register(extract_description_cmd, Command("description"))
    dp.message.register(list_attributes_elements_cmd, Command("list"))
    dp.message.register(list_attributes_cmd, Command("list_attributes"))
    dp.message.register(list_elements_cmd, Command("list_elements"))
    dp.message.register(max_cmd, Command("max"))
    dp.message.register(min_cmd, Command("min"))
    dp.message.register(mean_cmd, Command("mean"))
    dp.message.register(filter_cmd, Command("filter"))
    dp.message.register(stats_cmd, Command("stats"))
    dp.message.register(chart_cmd, Command("chart"))
    dp.message.register(chart_img_cmd, Command("chartimg"))
