from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
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

    if message.text.strip().lower() == "да":
        try:
            last_year = "2023-01-01"
            api_url = f"https://api.weatherapi.com/v1/history.json?key={config.Climate_API}&q={city}&dt={last_year}&lang=ru"
            response = requests.get(api_url)
            data = response.json()
            print(data)

            if "error" in data:
                bot.reply_to(message, "Не удалось получить климатические данные. Попробуйте позже.")
                return

            # Извлекаем климатические данные
            climate_info = data['forecast']['forecastday'][0]['day']
            avg_temp = climate_info['avgtemp_c']
            min_temp = climate_info['mintemp_c']
            max_temp = climate_info['maxtemp_c']
            avg_humidity = climate_info['avghumidity']

            bot.reply_to(message, f"🌎 Климат в **{city}** (1 января 2023):\n"
                                  f"📌 Средняя температура: {avg_temp}°C\n"
                                  f"🌡 Мин. температура: {min_temp}°C\n"
                                  f"🔥 Макс. температура: {max_temp}°C\n"
                                  f"💧 Средняя влажность: {avg_humidity}%\n"
                                  f"📊 Данные за прошлый год, чтобы дать общее представление о климате 🌍")

        except Exception as e:
            bot.reply_to(message, "Ошибка при получении климатических данных. Попробуйте позже.")
    else:
        bot.reply_to(message, "Хорошо! Если что, обращайтесь 😊")
