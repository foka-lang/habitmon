from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys
import logging
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

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

# URL твоего WebApp (корень сайта)
WEBAPP_URL = "https://habitmon-backend.onrender.com"

# ============================================================
# WEBHOOK
# ============================================================

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.headers.get('content-type') != 'application/json':
            return 'Unsupported content type', 400
        
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        
        if not update.message:
            return 'OK', 200
        
        text = update.message.text or ""
        chat_id = update.message.chat.id
        user_name = update.message.from_user.first_name or "Пользователь"
        
        logging.info(f"📝 Получено: '{text}' от {chat_id}")
        
        # ============================================================
        # ОТВЕТЫ
        # ============================================================
        
        if text.startswith('/start'):
            keyboard = InlineKeyboardMarkup(row_width=1)
            
            webapp_btn = InlineKeyboardButton(
                text="🚀 Открыть приложение",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
            
            help_btn = InlineKeyboardButton("❓ Помощь", callback_data="help")
            
            keyboard.add(webapp_btn, help_btn)
            
            welcome_text = f"""
🎯 Привет, {user_name}! 

Я бот HabitMon. Помогаю отслеживать привычки и достигать целей! 

Давай начнем твой путь к лучшей версии себя! 💪
"""
            
            bot.send_message(chat_id, welcome_text, reply_markup=keyboard)
            logging.info(f"✅ Отправлено приветствие для {chat_id}")
            
        elif text.startswith('/help') or text == '❓ Помощь':
            keyboard = InlineKeyboardMarkup(row_width=1)
            webapp_btn = InlineKeyboardButton(
                text="🚀 Открыть приложение",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
            keyboard.add(webapp_btn)
            
            help_text = """
🤖 Помощь по боту HabitMon:

/start - Запустить бота
/help - Показать это сообщение

📊 Бот помогает:
- Отслеживать ежедневные привычки
- Получать напоминания
- Следить за прогрессом
- Получать достижения
"""
            bot.send_message(chat_id, help_text, reply_markup=keyboard)
            logging.info(f"✅ Отправлена помощь для {chat_id}")
            
        else:
            keyboard = InlineKeyboardMarkup(row_width=1)
            webapp_btn = InlineKeyboardButton(
                text="🚀 Открыть приложение",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
            keyboard.add(webapp_btn)
            
            response_text = f"""
🤔 Я тебя не совсем понял.

Ты написал: "{text}"

Используй команды:
/start - Начать
/help - Помощь

Или нажми на кнопку ниже, чтобы открыть приложение! 🚀
"""
            bot.send_message(chat_id, response_text, reply_markup=keyboard)
            logging.info(f"ℹ️ Отправлен ответ на текст для {chat_id}")
        
        return 'OK', 200
        
    except Exception as e:
        logging.error(f"❌ Ошибка в webhook: {e}")
        return 'Error', 500

# ============================================================
# ФРОНТЕНД (index.html в КОРНЕ проекта)
# ============================================================

@app.route('/')
def home():
    # index.html лежит на уровень ВЫШЕ папки backend
    return send_from_directory('..', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    # Все остальные файлы (css, js) тоже ищем в корне
    return send_from_directory('..', path)

# ============================================================
# API ЭНДПОИНТЫ
# ============================================================

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
