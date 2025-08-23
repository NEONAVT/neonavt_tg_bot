import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo
from settings import settings

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    hello_button = types.InlineKeyboardButton(
        text="Open app",
        web_app=WebAppInfo(url="https://neonavt.github.io/neonavt_tg_bot/")
    )
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[hello_button]])
    await message.reply("Hello", reply_markup=markup)

@dp.message(F.web_app_data)
async def web_app(message: types.Message):
    await bot.send_message(message.chat.id, f"Данные получены: {message.web_app_data.data}")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))