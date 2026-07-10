from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)


# ============================================================
# API ЭНДПОИНТЫ
# ============================================================

@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "HabitMon API работает!",
        "bot": "запущен отдельно"
    })


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
        logging.error(f"Error in get_state: {e}")
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
        logging.error(f"Error in save_state: {e}")
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
        logging.error(f"Error in get_leaderboard: {e}")
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
        logging.error(f"Error in get_achievements: {e}")
        return jsonify({"error": str(e)}), 500


# ============================================================
# ЗАПУСК
# ============================================================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logging.info(f"🚀 Запускаем Flask на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)