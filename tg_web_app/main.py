import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo
from settings import settings

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Открыть",
                    web_app=WebAppInfo(url="https://neonavt.github.io/neonavt_tg_bot/")
                )
            ]
        ]
    )
    await message.answer("Жми кнопку", reply_markup=kb)

@dp.message()
async def get_data(message: types.Message):
    if message.web_app_data:
        await message.answer(f"Данные получены: {message.web_app_data.data}")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))