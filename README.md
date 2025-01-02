# Telegram Bot: WeatherBot

Этот Telegram-бот предоставляет информацию о текущей погоде в заданном городе.

## Описание

Бот принимает запросы от пользователей в виде названия города и возвращает информацию о текущей погоде в этом городе. Для получения данных используется API сервиса погоды.

## Функциональные возможности

- При отправке сообщения с названием города бот отвечает текущей погодой в этом городе.
- Для получения актуальной информации о погоде используется API сервиса (например, OpenWeatherMap).
- Бот обрабатывает запросы на русском и английском языках (по желанию).

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/EgorZybin/Weather_Telegram_Bot.git
   ```
2. Перейдите в директорию проекта:
   ```
   Weather_Telegram_Bot
   ```
3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
4. Получите API ключ для погодного сервиса
5. Создайте файл .env в корневой директории и добавьте следующий код:
   ```
   TELEGRAM_API_KEY="Ваш API ключ телеграмм"
   WEATHER_API_KEY="Ваш API ключ для погоды"
   ```
6. Запустите бота:
   ```
   python main.py
   ```

# Использование
Найдите бота в Telegram по имени или URL.
Отправьте название города (например, "Moscow" или "Москва").
Бот ответит текущей погодой в этом городе, включая температуру, влажность, описание погоды и другие данные.

