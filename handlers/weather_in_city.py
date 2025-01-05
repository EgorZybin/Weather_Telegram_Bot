from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import requests
from loader import bot
from config_data import config
import datetime
from database import save_request, get_user_history, init_db

user_city_data = {}

init_db()


@bot.message_handler(content_types=['text'])
def get_weather(message: Message) -> None:
    if message.text.startswith("/"):
        return

    try:
        city = message.text.strip()
        res = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.RAPID_API_KEY}&units=metric'
        )
        data = res.json()
        print(data)

        city_name = data['name']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        bot.reply_to(message, f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                              f"Погода в городе: {city_name}\nТемпература: {temperature}C°\n"
                              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
                              f"Продолжительность дня: {length_of_the_day}\n"
                              f"Хорошего дня!")

        # Сохраняем город для пользователя
        user_city_data[message.chat.id] = city
        save_request(message.chat.id, city_name, temperature)

        # Отправляем вопрос пользователю с кнопками "Да" и "Нет"
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_yes = KeyboardButton("Да")
        btn_no = KeyboardButton("Нет")
        markup.add(btn_yes, btn_no)

        bot.send_message(message.chat.id, "Хотите узнать климат в этом городе?", reply_markup=markup)

        # Переключаем обработчик на ожидание ответа пользователя
        bot.register_next_step_handler(message, get_climate)

    except Exception:
        bot.reply_to(message, "Проверьте название города.")


def get_climate(message: Message) -> None:
    """Получает климатические данные, если пользователь ответил 'Да'."""

    city = user_city_data.get(message.chat.id, None)

    if not city:
        bot.reply_to(message, "Произошла ошибка. Попробуйте снова.")
        return

    # 1. Получаем координаты города через OpenWeatherMap
    res = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.RAPID_API_KEY}&units=metric'
    )
    data = res.json()

    if res.status_code != 200 or "coord" not in data:
        bot.reply_to(message, "Не удалось получить координаты города. Попробуйте позже.")
        return

    # Извлекаем координаты
    lon = data['coord']['lon']
    lat = data['coord']['lat']

    # 2. Если пользователь подтвердил запрос, получаем климат по координатам
    if message.text.strip().lower() == "да":
        try:
            # Запрос к Open-Meteo API для получения климатических данных по координатам
            climate_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
            climate_response = requests.get(climate_url)
            climate_data = climate_response.json()

            if "error" in climate_data:
                bot.reply_to(message, "Не удалось получить климатические данные. Попробуйте позже.")
                return

            # Извлекаем климатические данные
            max_temp = climate_data['daily']['temperature_2m_max'][0]
            min_temp = climate_data['daily']['temperature_2m_min'][0]
            precipitation = climate_data['daily']['precipitation_sum'][0]

            # Форматируем ответ для пользователя
            response_message = (
                f"🌍 **Климат в городе {city}**:\n\n"
                f"📅 **Прогноз на ближайшие сутки**:\n\n"
                f"🌡 **Макс. температура**: {max_temp}°C\n"
                f"❄️ **Мин. температура**: {min_temp}°C\n"
                f"💧 **Осадки**: {precipitation} мм\n\n"
                f"📊 Эти данные могут помочь понять климатические условия города для планирования поездки.\n\n"
                f"Если вам нужно больше данных или другой прогноз, просто напишите! 😊"
            )

            bot.reply_to(message, response_message)

        except Exception as e:
            bot.reply_to(message, f"Ошибка при получении климатических данных. Попробуйте позже. Ошибка: {str(e)}")
    else:
        bot.reply_to(message, "Хорошо! Если что, обращайтесь 😊")