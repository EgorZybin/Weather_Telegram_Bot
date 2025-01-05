import sqlite3
import datetime


DB_PATH = './weather_bot.db'

def init_db():
    """Создает таблицу, если её нет"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            city TEXT,
            temperature REAL,
            request_date TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_request(user_id, city, temperature):
    """Сохраняет запрос пользователя в базу данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO history (user_id, city, temperature, request_date) 
        VALUES (?, ?, ?, ?)
    ''', (user_id, city, temperature, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


def get_user_history(user_id, limit=5):
    """Возвращает последние запросы пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT city, temperature, request_date FROM history
        WHERE user_id = ?
        ORDER BY request_date DESC
        LIMIT ?
    ''', (user_id, limit))
    history = cursor.fetchall()
    conn.close()
    return history
