import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode

from settings import settings

logging.basicConfig(level=logging.INFO)

bot = Bot(settings.bot_token)
dp = Dispatcher()


@dp.message(F.text == "/start")
async def start(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="Оформить заказ",
                web_app=WebAppInfo(url="https://neonavt.github.io/neonavt_tg_bot")
            )
        ]]
    )
    await message.answer("Нажми, чтобы оформить заказ:", reply_markup=kb)


@dp.message(F.web_app_data)
async def webapp_data(message: Message):
    logging.info("Получены данные web_app_data: %s", message.web_app_data.data)
    data = json.loads(message.web_app_data.data)
    text = (
        f"Получен заказ:\n"
        f"Имя: {data.get('name')}\n"
        f"Мейл: {data.get('email')}\n"
        f"Телефон: {data.get('phone')}"
    )
    await message.answer(text, parse_mode=ParseMode.HTML)



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
