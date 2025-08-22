from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from settings import settings
import asyncio

bot = Bot(settings.bot_token)
dp = Dispatcher()

# @dp.message(Command("start"))
# async def start(message: types.Message):
#     await message.reply("Hello")


@dp.message(F.photo)
async def get_photo(message: types.Message):
    await message.answer("Магия работает! Фото получено ✨")


@dp.message(Command("inline"))
async def info(message: types.Message):
    site_button = types.InlineKeyboardButton(text="Site", url="https://google.com")
    hello_button = types.InlineKeyboardButton(text="Hello", callback_data="Hello")

    markup = types.InlineKeyboardMarkup(inline_keyboard=[[site_button, hello_button]])

    await message.reply("Hello", reply_markup=markup)

@dp.message(Command("reply"))
async def reply(message: types.Message):
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Привет")],
            [types.KeyboardButton(text="Пока"), types.KeyboardButton(text="Как дела?")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("Выберите опцию:", reply_markup=markup)


@dp.callback_query()
async def callback(call: CallbackQuery):
    await call.message.answer(call.data)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))