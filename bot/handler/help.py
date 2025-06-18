from aiogram.types import Message




async def help_cmd(message: Message):
    await message.answer("📌 Commandes : /start /help")
