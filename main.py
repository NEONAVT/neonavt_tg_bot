import telebot
from telebot import types
from telebot.types import Message, CallbackQuery
import webbrowser
from settings import settings

bot = telebot.TeleBot(settings.bot_token)

@bot.message_handler(commands=["start"])
def main(message: Message):
    markup = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton("Go to website")
    button_3 = types.KeyboardButton("Delete photo")
    button_4 = types.KeyboardButton("Edit")
    markup.row(button_1)
    markup.row(button_3, button_4)
    with open("img.png", "rb") as file:
        bot.send_photo(message.chat.id, file, reply_markup=markup)
    # bot.send_message(message.chat.id,
    #                  f"Hello {message.from_user.first_name}"
    #                  f"{message.from_user.last_name if message.from_user.last_name is not None else ''}!",
    #                  reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message: Message):
    if message.text == "Go to website":
        webbrowser.open("https://itproger.com/course/telegram-bot/")
    elif message.text == "Delete photo":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=["site"])
def redirect_site(message: Message):
    webbrowser.open("https://itproger.com/course/telegram-bot/")

@bot.message_handler(content_types=["photo"])
def get_photo(message: Message):
    markup = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton("Go to website", url="https://itproger.com/course/telegram-bot/")
    button_3 = types.InlineKeyboardButton("Delete photo", callback_data="delete")
    button_4 = types.InlineKeyboardButton("Edit", callback_data="edit")
    markup.row(button_1, button_3, button_4)
    bot.reply_to(message, f"So beautiful photo", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback: CallbackQuery):
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == "edit":
        markup = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton("Go to website", url="https://itproger.com/course/telegram-bot/")
        button_3 = types.InlineKeyboardButton("Delete photo", callback_data="delete")
        button_4 = types.InlineKeyboardButton("Edit", callback_data="edit")
        markup.row(button_1, button_3, button_4)
        bot.edit_message_text("Edit text", callback.message.chat.id, callback.message.message_id, reply_markup=markup)


@bot.message_handler()
def info(message: Message):
    if "привет" in message.text.lower():
        bot.send_message(message.chat.id,
                         f"Hello {message.from_user.first_name}"
                         f"{message.from_user.last_name if message.from_user.last_name is not None else ''}!")
    elif "id" in message.text.lower():
        bot.reply_to(message, f"Твой ID: {message.from_user.id}")


if __name__ == "__main__":
    bot.polling(non_stop=True)
