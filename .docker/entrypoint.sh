echo "📦 Инициализация базы данных..."
python -c "from database import init_db; init_db()"

echo "🚀 Запуск бота..."
exec python main.py

