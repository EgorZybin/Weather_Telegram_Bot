from telebot.types import Message
import requests
from loader import bot
from config_data import config
import datetime


@bot.message_handler(content_types=['text'])
def get_weather(message: Message) -> None:
    try:
        res = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={config.RAPID_API_KEY}&units'
            f'=metric')
        data = res.json()
        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])
        bot.reply_to(message, f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                              f"Погода в городе: {city}\nТемпература: {cur_weather}C°\n"
                              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
                              f"Продолжительность дня: {length_of_the_day}\n"
                              f"Хорошего дня!")
    except Exception:
        bot.reply_to(message, "Проверьте название города.")
