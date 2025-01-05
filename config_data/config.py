import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BotToken')
RAPID_API_KEY = os.getenv('API_Key')
Climate_API = os.getenv('Climate_API')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Помощь по командам бота"),
    ('history', "Показать историю запросов"),
)
