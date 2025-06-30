from bot.handler.start import start_cmd
from bot.handler.help import help_cmd
from aiogram.filters import Command
from bot.handler.settings import modifier_data
from bot.handler.search.search_cmd import search_cmd
from bot.handler.extract.extract_cmd import extract_cmd, extract_description_cmd, list_attributes_elements_cmd, list_attributes_cmd, list_elements_cmd


def register_handlers(dp):
    dp.message.register(start_cmd, Command("start"))
    dp.message.register(help_cmd, Command("help"))
    dp.message.register(modifier_data, Command("modifier"))
    dp.message.register(search_cmd, Command("search"))
    dp.message.register(extract_cmd, Command("extract"))
    dp.message.register(extract_description_cmd, Command("description"))
    dp.message.register(list_attributes_elements_cmd, Command("list"))
    dp.message.register(list_attributes_cmd, Command("list_attributes"))
    dp.message.register(list_elements_cmd, Command("list_elements"))
