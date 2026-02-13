import os
import telebot

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Как тебя зовут?")
    user_data[message.chat.id] = {"step": "name"}


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        bot.send_message(chat_id, "Напиши /start")
        return

    step = user_data[chat_id]["step"]

    if step == "name":
        user_data[chat_id]["name"] = message.text
        user_data[chat_id]["step"] = "age"
        bot.send_message(chat_id, "Сколько тебе лет?")

    elif step == "age":
        if not message.text.isdigit():
            bot.send_message(chat_id, "Введи возраст цифрами")
            return

        name = user_data[chat_id]["name"]
        age = message.text

        bot.send_message(
            chat_id,
            f"Тебя зовут {name}, тебе {age} лет"
        )

        del user_data[chat_id]


print("Бот запущен...")
bot.polling()