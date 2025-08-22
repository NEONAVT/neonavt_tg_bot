import telebot
from telebot.types import Message
import requests

from settings import settings

bot = telebot.TeleBot(token=settings.bot_token)

@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.send_message(message.chat.id, text="Привет! Напиши название города.")

@bot.message_handler(content_types=["text"])
def get_weather(message: Message):
    city_name = message.text.strip().lower()
    weather_url = requests.get(settings.weather_url(city_name))
    if weather_url.status_code == 200:
        weather_data = weather_url.json()
        bot.reply_to(message, text=f"Погода в {weather_data["name"]}\n"
                                   f"Температура воздуха: {weather_data["main"]["temp"]} °C\n"
                                   f"Ощущается как: {weather_data["main"]["feels_like"]} °C\n"
                                   f"Давление: {weather_data["main"]["pressure"]} мм рт. ст.\n"
                                   f"Ветер: {weather_data["wind"]["speed"]} м\сек\n"
                                   f"Небо: {weather_data["weather"][0]["description"]}\n")
    else:
        bot.send_message(message.chat.id, text=f"{city_name.capitalize()} - не верное название города. Попробуйте снова.")


if __name__ == "__main__":
    bot.polling(non_stop=True)