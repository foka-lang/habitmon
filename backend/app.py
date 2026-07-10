from flask import Flask, jsonify, request
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

# URL твоего WebApp (мини-приложения)
# Если у тебя фронтенд лежит в том же репозитории, он доступен по тому же адресу
WEBAPP_URL = "https://habitmon-backend.onrender.com"  # Или отдельный URL, если фронтенд отдельно

# ============================================================
# ВСЯ ЛОГИКА БОТА В WEBHOOK
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
        # СОЗДАЁМ КРАСИВЫЕ КНОПКИ
        # ============================================================
        
        if text.startswith('/start'):
            # Создаём клавиатуру с кнопками
            keyboard = InlineKeyboardMarkup(row_width=2)
            
            # Кнопка для открытия приложения
            webapp_btn = InlineKeyboardButton(
                text="🚀 Открыть приложение",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
            
            # Кнопки с командами
            habits_btn = InlineKeyboardButton("📋 Мои привычки", callback_data="habits")
            stats_btn = InlineKeyboardButton("📊 Статистика", callback_data="stats")
            menu_btn = InlineKeyboardButton("📌 Меню", callback_data="menu")
            help_btn = InlineKeyboardButton("❓ Помощь", callback_data="help")
            
            # Добавляем кнопки в клавиатуру
            keyboard.add(webapp_btn)
            keyboard.add(habits_btn, stats_btn)
            keyboard.add(menu_btn, help_btn)
            
            # Текст приветствия
            welcome_text = f"""
🎯 Привет, {user_name}! 

Я бот HabitMon. Помогаю отслеживать привычки и достигать целей!

Нажми на кнопку ниже, чтобы открыть приложение, или используй команды:
/start - Показать это сообщение
/help - Помощь
/menu - Главное меню
/stats - Моя статистика

Давай начнем твой путь к лучшей версии себя! 💪
"""
            
            bot.send_message(chat_id, welcome_text, reply_markup=keyboard)
            logging.info(f"✅ Отправлено приветствие с кнопками для {chat_id}")
            
        elif text.startswith('/help'):
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
/menu - Открыть главное меню
/stats - Показать мою статистику

📊 Бот помогает:
- Отслеживать ежедневные привычки
- Получать напоминания
- Следить за прогрессом
- Получать достижения
"""
            bot.send_message(chat_id, help_text, reply_markup=keyboard)
            logging.info(f"✅ Отправлена помощь для {chat_id}")
            
        elif text.startswith('/menu'):
            keyboard = InlineKeyboardMarkup(row_width=1)
            webapp_btn = InlineKeyboardButton(
                text="🚀 Открыть приложение",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
            keyboard.add(webapp_btn)
            
            menu_text = """
📋 ГЛАВНОЕ МЕНЮ:

1️⃣ Мои привычки
2️⃣ Добавить привычку
3️⃣ Моя статистика
4️⃣ Достижения
5️⃣ Лидерборд
6️⃣ Настройки

Нажми на кнопку ниже, чтобы открыть приложение! 🚀
"""
            bot.send_message(chat_id, menu_text, reply_markup=keyboard)
            logging.info(f"✅ Отправлено меню для {chat_id}")
            
        elif text.startswith('/stats'):
            keyboard = InlineKeyboardMarkup(row_width=1)
            webapp_btn = InlineKeyboardButton(
                text="🚀 Открыть приложение",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
            keyboard.add(webapp_btn)
            
            stats_text = """
📊 МОЯ СТАТИСТИКА:

🔹 Уровень: 1
🔹 Опыт: 0 / 100
🔹 Очки: 0
🔹 Дней в серии: 0
🔹 Выполнено привычек: 0

Продолжай в том же духе! 💪
"""
            bot.send_message(chat_id, stats_text, reply_markup=keyboard)
            logging.info(f"✅ Отправлена статистика для {chat_id}")
            
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
/menu - Меню
/stats - Статистика

Или нажми на кнопку ниже, чтобы открыть приложение! 🚀
"""
            bot.send_message(chat_id, response_text, reply_markup=keyboard)
            logging.info(f"ℹ️ Отправлен ответ на текст для {chat_id}")
        
        return 'OK', 200
        
    except Exception as e:
        logging.error(f"❌ Ошибка в webhook: {e}")
        return 'Error', 500

# ============================================================
# ОБРАБОТКА НАЖАТИЙ НА КНОПКИ (callback)
# ============================================================

@app.route('/webhook', methods=['POST'])
def webhook_callback():
    # Тут можно обрабатывать нажатия на кнопки (callback_data)
    # Но для простоты пока пропустим
    pass

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
