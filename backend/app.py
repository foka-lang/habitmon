from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
import logging
import telebot

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

# ============================================================
# ТЕЛЕГРАМ БОТ
# ============================================================

# Получаем токен из переменных окружения
bot_token = os.getenv('bot_token')

if not bot_token:
    logging.error("❌ bot_token не найден в переменных окружения!")
    logging.error("Пожалуйста, добавьте bot_token в Environment переменные на Render")
else:
    logging.info("✅ bot_token загружен успешно")

# Инициализация бота
bot = telebot.TeleBot(bot_token)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user_name = message.from_user.first_name if message.from_user.first_name else "Пользователь"
        welcome_text = f"""
🎯 Привет, {user_name}! 

Я бот HabitMon. Помогаю отслеживать привычки и достигать целей!

📌 Доступные команды:
/start - Показать это сообщение
/help - Помощь
/menu - Главное меню
/stats - Моя статистика

Давай начнем твой путь к лучшей версии себя! 💪
"""
        bot.send_message(message.chat.id, welcome_text)
        logging.info(f"✅ Команда /start от {user_name} (ID: {message.from_user.id}) обработана успешно")
    except Exception as e:
        logging.error(f"❌ Ошибка в send_welcome: {e}")
        bot.send_message(message.chat.id, "Извините, произошла ошибка. Попробуйте позже.")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    try:
        help_text = """
🤖 Помощь по боту HabitMon:

/start - Запустить бота
/help - Показать это сообщение
/menu - Открыть главное меню
/stats - Показать мою статистику

📊 Бот помогает:
- Отслеживать ежедневные привычки
- Получать напоминания
- Следить за прогрессом
- Получать достижения

Есть вопросы? Обращайтесь к разработчику!
"""
        bot.send_message(message.chat.id, help_text)
        logging.info(f"✅ Команда /help от {message.from_user.id} обработана")
    except Exception as e:
        logging.error(f"❌ Ошибка в send_help: {e}")
        bot.send_message(message.chat.id, "Извините, произошла ошибка. Попробуйте позже.")

# Обработчик команды /menu
@bot.message_handler(commands=['menu'])
def send_menu(message):
    try:
        menu_text = """
📋 ГЛАВНОЕ МЕНЮ:

1️⃣ Мои привычки
2️⃣ Добавить привычку
3️⃣ Моя статистика
4️⃣ Достижения
5️⃣ Лидерборд
6️⃣ Настройки

В разработке! Скоро будут доступны все функции. 🚀
"""
        bot.send_message(message.chat.id, menu_text)
        logging.info(f"✅ Команда /menu от {message.from_user.id} обработана")
    except Exception as e:
        logging.error(f"❌ Ошибка в send_menu: {e}")
        bot.send_message(message.chat.id, "Извините, произошла ошибка. Попробуйте позже.")

# Обработчик команды /stats
@bot.message_handler(commands=['stats'])
def send_stats(message):
    try:
        stats_text = """
📊 МОЯ СТАТИСТИКА:

🔹 Уровень: 1
🔹 Опыт: 0 / 100
🔹 Очки: 0
🔹 Дней в серии: 0
🔹 Выполнено привычек: 0

Продолжай в том же духе! 💪
"""
        bot.send_message(message.chat.id, stats_text)
        logging.info(f"✅ Команда /stats от {message.from_user.id} обработана")
    except Exception as e:
        logging.error(f"❌ Ошибка в send_stats: {e}")
        bot.send_message(message.chat.id, "Извините, произошла ошибка. Попробуйте позже.")

# Обработчик текстовых сообщений (если пользователь написал что-то другое)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        response_text = f"""
🤔 Я тебя не совсем понял.

Ты написал: "{message.text}"

Чтобы я понимал твои команды, используй кнопки меню или команды:
/start - Начать
/help - Помощь
/menu - Меню
/stats - Статистика
"""
        bot.send_message(message.chat.id, response_text)
        logging.info(f"ℹ️ Сообщение от {message.from_user.id}: {message.text}")
    except Exception as e:
        logging.error(f"❌ Ошибка в echo_all: {e}")
        bot.send_message(message.chat.id, "Извините, произошла ошибка. Попробуйте позже.")

# ============================================================
# API ЭНДПОИНТЫ
# ============================================================

@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "HabitMon API работает!",
        "bot": "Telegram бот запущен и готов к работе"
    })

# Webhook для Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            logging.info(f"✅ Webhook обработал запрос от Telegram")
            return 'OK', 200
        else:
            logging.warning(f"⚠️ Webhook получил запрос с неправильным content-type: {request.headers.get('content-type')}")
            return 'Unsupported content type', 400
    except Exception as e:
        logging.error(f"❌ Ошибка в webhook: {e}")
        return 'Error processing webhook', 500

# Получение состояния пользователя
@app.route('/api/state', methods=['POST'])
def get_state():
    try:
        data = request.get_json()
        telegram_id = data.get('telegram_id')

        if not telegram_id:
            return jsonify({"error": "telegram_id required"}), 400

        # Здесь будет запрос к базе данных
        return jsonify({
            "status": "ok",
            "user": {
                "telegram_id": telegram_id,
                "username": "test_user",
                "level": 1,
                "xp": 0,
                "points": 0
            },
            "habits": [],
            "subscription": None
        })
    except Exception as e:
        logging.error(f"❌ Ошибка в get_state: {e}")
        return jsonify({"error": str(e)}), 500

# Сохранение состояния пользователя
@app.route('/api/state/save', methods=['POST'])
def save_state():
    try:
        data = request.get_json()
        telegram_id = data.get('telegram_id')
        state = data.get('state')

        if not telegram_id or not state:
            return jsonify({"error": "telegram_id and state required"}), 400

        # Здесь будет сохранение в базу данных
        return jsonify({
            "status": "ok",
            "message": "Данные сохранены"
        })
    except Exception as e:
        logging.error(f"❌ Ошибка в save_state: {e}")
        return jsonify({"error": str(e)}), 500

# Получение лидерборда
@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        # Демо-данные для лидерборда
        leaderboard = [
            {"username": "Алексей", "points": 450},
            {"username": "Мария", "points": 420},
            {"username": "Игорь", "points": 380},
            {"username": "Ольга", "points": 300},
            {"username": "Сергей", "points": 280}
        ]
        return jsonify({
            "status": "ok",
            "leaderboard": leaderboard
        })
    except Exception as e:
        logging.error(f"❌ Ошибка в get_leaderboard: {e}")
        return jsonify({"error": str(e)}), 500

# Получение достижений пользователя
@app.route('/api/achievements', methods=['POST'])
def get_achievements():
    try:
        data = request.get_json()
        telegram_id = data.get('telegram_id')

        if not telegram_id:
            return jsonify({"error": "telegram_id required"}), 400

        # Демо-достижения
        achievements = [
            {"id": "first", "name": "Первый шаг", "desc": "Добавить первую привычку", "unlocked": False},
            {"id": "week_streak", "name": "Неделя дисциплины", "desc": "Серия 7 дней", "unlocked": False},
            {"id": "month_streak", "name": "Месяц силы воли", "desc": "Серия 30 дней", "unlocked": False}
        ]
        return jsonify({
            "status": "ok",
            "achievements": achievements
        })
    except Exception as e:
        logging.error(f"❌ Ошибка в get_achievements: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logging.info(f"🚀 Запускаем Flask на порту {port}")
    logging.info(f"🤖 Telegram бот инициализирован")
    logging.info(f"📡 Webhook будет доступен по адресу: https://habitmon-backend.onrender.com/webhook")
    app.run(host='0.0.0.0', port=port, debug=False)
