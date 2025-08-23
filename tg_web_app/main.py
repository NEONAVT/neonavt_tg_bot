import asyncio
import logging
from os import getenv

import dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup

dotenv.load_dotenv()

API_TOKEN = getenv('BOT_TOKEN')
WEBAPP_URL = getenv('WEB_APP_URL')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def start(message: types.Message):
    """Handle the /start command from user and print custom keyboard."""
    kb = [
        [
            types.KeyboardButton(text="🚀 Launch WebApp", web_app=WebAppInfo(url=WEBAPP_URL))
        ],
        [
            types.KeyboardButton(text="ℹ️ Information")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Choose an action"
    )
    await message.answer("Welcome! Choose an action:", reply_markup=keyboard)


@dp.message(F.text == "ℹ️ Information")
async def info(message: types.Message):
    """Handle the information button and print predefined message."""
    await message.answer("This is a Telegram bot with a WebApp interface. Click the first button to launch the WebApp.")


# @dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    """Handle data sent from the WebApp."""
    await message.answer(f"✅ Data received from WebApp:\n{message.web_app_data.data}")


async def main() -> None:
    """Start the bot."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())