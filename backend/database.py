import sqlite3

DB_PATH = 'habits.db'


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       telegram_id
                       INTEGER
                       UNIQUE
                       NOT
                       NULL,
                       username
                       TEXT,
                       full_name
                       TEXT,
                       theme
                       TEXT
                       DEFAULT
                       'white',
                       language
                       TEXT
                       DEFAULT
                       'ru',
                       notification_enabled
                       INTEGER
                       DEFAULT
                       1,
                       current_streak
                       INTEGER
                       DEFAULT
                       0,
                       max_streak
                       INTEGER
                       DEFAULT
                       0,
                       last_activity_date
                       TEXT,
                       created_at
                       TEXT
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   ''')

    # Таблица привычек
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS habits
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       user_id
                       INTEGER
                       NOT
                       NULL,
                       name
                       TEXT
                       NOT
                       NULL,
                       emoji
                       TEXT
                       DEFAULT
                       '📌',
                       frequency
                       TEXT
                       DEFAULT
                       'daily',
                       custom_days
                       TEXT,
                       reminder_time
                       TEXT,
                       is_active
                       INTEGER
                       DEFAULT
                       1,
                       created_at
                       TEXT
                       DEFAULT
                       CURRENT_TIMESTAMP,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   ) ON DELETE CASCADE
                       )
                   ''')

    # Таблица логов привычек
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS habit_logs
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       habit_id
                       INTEGER
                       NOT
                       NULL,
                       date
                       TEXT
                       NOT
                       NULL,
                       completed
                       INTEGER
                       DEFAULT
                       0,
                       note
                       TEXT,
                       FOREIGN
                       KEY
                   (
                       habit_id
                   ) REFERENCES habits
                   (
                       id
                   ) ON DELETE CASCADE
                       )
                   ''')

    # Таблица челленджей
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS challenges
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       name
                       TEXT
                       NOT
                       NULL,
                       habit_id
                       INTEGER
                       NOT
                       NULL,
                       creator_id
                       INTEGER
                       NOT
                       NULL,
                       start_date
                       TEXT
                       NOT
                       NULL,
                       end_date
                       TEXT
                       NOT
                       NULL,
                       type
                       TEXT
                       DEFAULT
                       'count',
                       status
                       TEXT
                       DEFAULT
                       'active',
                       FOREIGN
                       KEY
                   (
                       habit_id
                   ) REFERENCES habits
                   (
                       id
                   ) ON DELETE CASCADE,
                       FOREIGN KEY
                   (
                       creator_id
                   ) REFERENCES users
                   (
                       id
                   )
                     ON DELETE CASCADE
                       )
                   ''')

    # Таблица участников челленджей
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS challenge_participants
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       challenge_id
                       INTEGER
                       NOT
                       NULL,
                       user_id
                       INTEGER
                       NOT
                       NULL,
                       progress
                       INTEGER
                       DEFAULT
                       0,
                       joined_at
                       TEXT
                       DEFAULT
                       CURRENT_TIMESTAMP,
                       FOREIGN
                       KEY
                   (
                       challenge_id
                   ) REFERENCES challenges
                   (
                       id
                   ) ON DELETE CASCADE,
                       FOREIGN KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   )
                     ON DELETE CASCADE
                       )
                   ''')

    # Таблица рефералов
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS referrals
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       referrer_id
                       INTEGER
                       NOT
                       NULL,
                       referred_id
                       INTEGER
                       NOT
                       NULL,
                       bonus_points
                       INTEGER
                       DEFAULT
                       250,
                       created_at
                       TEXT
                       DEFAULT
                       CURRENT_TIMESTAMP,
                       FOREIGN
                       KEY
                   (
                       referrer_id
                   ) REFERENCES users
                   (
                       id
                   ) ON DELETE CASCADE,
                       FOREIGN KEY
                   (
                       referred_id
                   ) REFERENCES users
                   (
                       id
                   )
                     ON DELETE CASCADE
                       )
                   ''')

    # Таблица подписок
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS subscriptions
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       user_id
                       INTEGER
                       NOT
                       NULL,
                       plan
                       TEXT
                       NOT
                       NULL,
                       price_stars
                       INTEGER
                       NOT
                       NULL,
                       start_date
                       TEXT
                       NOT
                       NULL,
                       end_date
                       TEXT
                       NOT
                       NULL,
                       is_active
                       INTEGER
                       DEFAULT
                       1,
                       payment_id
                       TEXT,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   ) ON DELETE CASCADE
                       )
                   ''')

    # Таблица дневной статистики
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS daily_stats
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       user_id
                       INTEGER
                       NOT
                       NULL,
                       date
                       TEXT
                       NOT
                       NULL,
                       total_habits
                       INTEGER
                       DEFAULT
                       0,
                       completed_habits
                       INTEGER
                       DEFAULT
                       0,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   ) ON DELETE CASCADE
                       )
                   ''')

    # Таблица глобальных челленджей
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS global_challenges
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       month
                       TEXT
                       NOT
                       NULL,
                       start_date
                       TEXT
                       NOT
                       NULL,
                       end_date
                       TEXT
                       NOT
                       NULL,
                       status
                       TEXT
                       DEFAULT
                       'active'
                   )
                   ''')

    # Таблица очков глобальных челленджей
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS global_challenge_scores
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       challenge_id
                       INTEGER
                       NOT
                       NULL,
                       user_id
                       INTEGER
                       NOT
                       NULL,
                       total_completed
                       INTEGER
                       DEFAULT
                       0,
                       FOREIGN
                       KEY
                   (
                       challenge_id
                   ) REFERENCES global_challenges
                   (
                       id
                   ) ON DELETE CASCADE,
                       FOREIGN KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   )
                     ON DELETE CASCADE
                       )
                   ''')

    # Таблица баллов пользователя
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS user_points
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       user_id
                       INTEGER
                       NOT
                       NULL
                       UNIQUE,
                       total_points
                       INTEGER
                       DEFAULT
                       0,
                       updated_at
                       TEXT
                       DEFAULT
                       CURRENT_TIMESTAMP,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   ) ON DELETE CASCADE
                       )
                   ''')

    # Таблица наград за топ-10
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS monthly_rewards
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       user_id
                       INTEGER
                       NOT
                       NULL,
                       month
                       TEXT
                       NOT
                       NULL,
                       place
                       INTEGER
                       NOT
                       NULL,
                       reward_points
                       INTEGER
                       NOT
                       NULL,
                       created_at
                       TEXT
                       DEFAULT
                       CURRENT_TIMESTAMP,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   ) ON DELETE CASCADE
                       )
                   ''')

    # Таблица уровней пользователя
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS user_levels
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       user_id
                       INTEGER
                       NOT
                       NULL
                       UNIQUE,
                       level
                       INTEGER
                       DEFAULT
                       1,
                       xp
                       INTEGER
                       DEFAULT
                       0,
                       total_xp_earned
                       INTEGER
                       DEFAULT
                       0,
                       updated_at
                       TEXT
                       DEFAULT
                       CURRENT_TIMESTAMP,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   ) ON DELETE CASCADE
                       )
                   ''')

    # Таблица наград за стрики
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS streak_rewards
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       user_id
                       INTEGER
                       NOT
                       NULL,
                       streak_days
                       INTEGER
                       NOT
                       NULL,
                       reward_xp
                       INTEGER
                       NOT
                       NULL,
                       reward_points
                       INTEGER
                       NOT
                       NULL,
                       created_at
                       TEXT
                       DEFAULT
                       CURRENT_TIMESTAMP,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   ) ON DELETE CASCADE
                       )
                   ''')

    conn.commit()
    conn.close()
    print("✅ База данных успешно создана!")


if __name__ == '__main__':
    init_db()