import telebot
from telebot.types import Message
import webbrowser
from settings import settings

bot = telebot.TeleBot(settings.bot_token)

@bot.message_handler(commands=["start"])
def main(message: Message):
    bot.send_message(message.chat.id,
                     f"Hello {message.from_user.first_name}"
                     f"{message.from_user.last_name if message.from_user.last_name is not None else ''}!")

@bot.message_handler(commands=["site"])
def redirect_site(message: Message):
    webbrowser.open("https://itproger.com/course/telegram-bot/")

@bot.message_handler()
def info(message: Message):
    if "привет" in message.text.lower():
        bot.send_message(message.chat.id,
                         f"Hello {message.from_user.first_name}"
                         f"{message.from_user.last_name if message.from_user.last_name is not None else ''}!")
    elif "id" in message.text.lower():
        bot.reply_to(message, f"Твой ID: {message.from_user.id}")


if __name__ == "__main__":
    bot.infinity_polling(timeout=20)
