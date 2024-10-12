from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    bot.reply_to(message,
                 f"Привет, рад тебя видеть. Я бот-помощник. Напиши название города. Чтобы увидеть полный список моих "
                 f"функций, напишите /help.")
