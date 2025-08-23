import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from settings import settings

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Открыть", web_app=WebAppInfo(url="https://neonavt.github.io/neonavt_tg_bot/"))
        ],

    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Choose an action"
    )
    await message.answer("Welcome! Choose an action:", reply_markup=keyboard)

@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    """Handle data sent from the WebApp."""
    await message.answer(f"✅ Data received from WebApp:\n{message.web_app_data.data}")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))