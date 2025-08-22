import telebot
from telebot.types import Message, CallbackQuery
from telebot import types

from settings import settings
from currency_converter import CurrencyConverter

amount = 0

bot = telebot.TeleBot(settings.bot_token)
currency = CurrencyConverter()

@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.send_message(message.chat.id, text="Введите сумму.")
    bot.register_next_step_handler(message, summa)


def summa(message: Message):
    global amount
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            bot.send_message(message.chat.id, "Число должно быть положительным!")
            bot.register_next_step_handler(message, summa)
            return
    except ValueError:
        bot.send_message(message.chat.id, "Введите целое число!")
        bot.register_next_step_handler(message, summa)
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    usd_eur = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
    eur_usd = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
    usd_gbp = types.InlineKeyboardButton("USD/GBP", callback_data="usd/gbp")
    users_currency = types.InlineKeyboardButton("Другое значение", callback_data="else")
    markup.add(usd_eur, eur_usd, usd_gbp, users_currency)
    bot.send_message(message.chat.id, "Выберите пару валют для расчета.", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call: CallbackQuery):
    if call.data != "else":
        values = call.data.upper().split("/")
        try:
            convert = currency.convert(amount, values[0], values[1])
            bot.send_message(
                call.message.chat.id,
                text=f"Результат конвертации суммы {amount} с {values[0]} на {values[1]}: {round(convert, 2)}\n"
            )
        except Exception as e:
            bot.send_message(call.message.chat.id, f"Ошибка: {e}. Попробуйте другую пару.")
            bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Введите пару валют через слэш (например, RUB/USD):")
        bot.register_next_step_handler(call.message, handle_custom_currency)


def handle_custom_currency(message: Message):
    try:
        values = message.text.upper().strip().split("/")
        if len(values) != 2:
            bot.send_message(message.chat.id, "Введите две валюты через слэш (например, RUB/UAH)")
            bot.register_next_step_handler(message, handle_custom_currency)
            return

        from_currency, to_currency = values[0], values[1]
        convert = currency.convert(amount, from_currency, to_currency)

        bot.send_message(
            message.chat.id,
            text=f"Результат конвертации суммы {amount} с {from_currency} на {to_currency}: {round(convert, 2)}\n"
                 f"Для продолжения введите новую сумму:"
        )
        bot.register_next_step_handler(message, summa)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}. Проверьте название валют (например, USD, EUR, RUB, UAH).")
        bot.register_next_step_handler(message, handle_custom_currency)


bot.polling(non_stop=True)