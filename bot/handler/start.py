from aiogram.types import Message



async def start_cmd(message: Message):
    await message.answer("👋 Bienvenue sur ton bot !\nTape /amazon ou /cdiscount")
