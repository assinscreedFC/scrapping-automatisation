from bot.handler.start import start_cmd
from bot.handler.help import help_cmd
from aiogram.filters import Command
from bot.handler.settings import modifier_data


def register_handlers(dp):
    dp.message.register(start_cmd, Command("start"))
    dp.message.register(help_cmd, Command("help"))
    dp.message.register(modifier_data, Command("modifier"))
