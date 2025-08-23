import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo
from settings import settings

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    hello_button = types.InlineKeyboardButton(text="Open app", web_app=WebAppInfo(url="https://www.youtube.com"))
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[hello_button]])
    await message.reply("Hello", reply_markup=markup)


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))