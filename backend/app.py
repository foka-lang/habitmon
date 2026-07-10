from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
import logging
import telebot

# ============================================================
# НАСТРОЙКА
# ============================================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

# ============================================================
# ТЕЛЕГРАМ БОТ
# ============================================================
bot_token = os.getenv('bot_token')

if not bot_token:
    logging.error("❌ bot_token не найден в переменных окружения!")
else:
    logging.info("✅ bot_token загружен успешно")

bot = telebot.TeleBot(bot_token)

# ============================================================
# ВСЯ ЛОГИКА БОТА В ОДНОМ МЕСТЕ (webhook)
# ============================================================

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.headers.get('content-type') != 'application/json':
            return 'Unsupported content type', 400
        
        # Получаем данные от Telegram
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        
        if not update.message:
            return 'OK', 200
        
        # Извлекаем данные
        text = update.message.text or ""
        chat_id = update.message.chat.id
        user_name = update.message.from_user.first_name or "Пользователь"
        
        logging.info(f"📝 Получено: '{text}' от {chat_id}")
        
        # ============================================================
        # ОБРАБОТКА КОМАНД (прямая, без @bot.message_handler)
        # ============================================================
        
        response_text = ""
        
        if text.startswith('/start'):
            response_text = f"""
🎯 Привет, {user_name}! 

Я бот HabitMon. Помогаю отслеживать привычки и достигать целей!

📌 Доступные команды:
/start - Показать это сообщение
/help - Помощь
/menu - Главное меню
/stats - Моя статистика

Давай начнем твой путь к лучшей версии себя! 💪
"""
            logging.info(f"✅ Обработана команда /start для {chat_id}")
            
        elif text.startswith('/help'):
            response_text = """
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
"""
            logging.info(f"✅ Обработана команда /help для {chat_id}")
            
        elif text.startswith('/menu'):
            response_text = """
📋 ГЛАВНОЕ МЕНЮ:

1️⃣ Мои привычки
2️⃣ Добавить привычку
3️⃣ Моя статистика
4️⃣ Достижения
5️⃣ Лидерборд
6️⃣ Настройки

В разработке! Скоро будут доступны все функции. 🚀
"""
            logging.info(f"✅ Обработана команда /menu для {chat_id}")
            
        elif text.startswith('/stats'):
            response_text = """
📊 МОЯ СТАТИСТИКА:

🔹 Уровень: 1
🔹 Опыт: 0 / 100
🔹 Очки: 0
🔹 Дней в серии: 0
🔹 Выполнено привычек: 0

Продолжай в том же духе! 💪
"""
            logging.info(f"✅ Обработана команда /stats для {chat_id}")
            
        else:
            response_text = f"""
🤔 Я тебя не совсем понял.

Ты написал: "{text}"

Используй команды:
/start - Начать
/help - Помощь
/menu - Меню
/stats - Статистика
"""
            logging.info(f"ℹ️ Обработано текстовое сообщение от {chat_id}")
        
        # ============================================================
        # ОТПРАВКА ОТВЕТА
        # ============================================================
        
        if response_text:
            bot.send_message(chat_id, response_text)
            logging.info(f"✅ Ответ отправлен пользователю {chat_id}")
        
        return 'OK', 200
        
    except Exception as e:
        logging.error(f"❌ Ошибка в webhook: {e}")
        return 'Error', 500

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

@app.route('/api/state', methods=['POST'])
def get_state():
    try:
        data = request.get_json()
        telegram_id = data.get('telegram_id')
        if not telegram_id:
            return jsonify({"error": "telegram_id required"}), 400
        return jsonify({
            "status": "ok",
            "user": {"telegram_id": telegram_id, "username": "test_user", "level": 1, "xp": 0, "points": 0},
            "habits": [],
            "subscription": None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/state/save', methods=['POST'])
def save_state():
    try:
        data = request.get_json()
        telegram_id = data.get('telegram_id')
        state = data.get('state')
        if not telegram_id or not state:
            return jsonify({"error": "telegram_id and state required"}), 400
        return jsonify({"status": "ok", "message": "Данные сохранены"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    return jsonify({
        "status": "ok",
        "leaderboard": [
            {"username": "Алексей", "points": 450},
            {"username": "Мария", "points": 420},
            {"username": "Игорь", "points": 380}
        ]
    })

@app.route('/api/achievements', methods=['POST'])
def get_achievements():
    return jsonify({
        "status": "ok",
        "achievements": [
            {"id": "first", "name": "Первый шаг", "desc": "Добавить первую привычку", "unlocked": False},
            {"id": "week_streak", "name": "Неделя дисциплины", "desc": "Серия 7 дней", "unlocked": False}
        ]
    })

# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logging.info(f"🚀 Запускаем Flask на порту {port}")
    logging.info(f"🤖 Telegram бот инициализирован")
    logging.info(f"📡 Webhook: https://habitmon-backend.onrender.com/webhook")
    app.run(host='0.0.0.0', port=port, debug=False)
