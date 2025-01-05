from telebot.types import Message
from database import get_user_history
from loader import bot


@bot.message_handler(commands=['history'])
def show_history(message: Message) -> None:
    """Показывает историю запросов пользователя"""
    history = get_user_history(message.chat.id)

    if not history:
        bot.reply_to(message, "📜 Ваша история запросов пуста. Попробуйте сначала узнать погоду!")
        return

    history_text = "📜 История ваших последних запросов:\n"
    for city, temp, date in history:
        history_text += f"🌍 {city}: {temp}°C ({date})\n"

    bot.reply_to(message, history_text)
